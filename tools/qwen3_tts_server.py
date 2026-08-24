"""Local Qwen3-TTS Base voice-cloning service for LiveTalking and web/tts."""

from __future__ import annotations

import argparse
import io
import json
import re
import threading
import time
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf
import torch
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_DIR = ROOT / "models" / "qwen3-tts-0.6b-base"
DEFAULT_VOICE_DIR = ROOT / "models" / "qwen3-tts-voices"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class SpeechRequest(BaseModel):
    input: str = Field(min_length=1, max_length=10_000)
    voice: str = ""
    response_format: str = "pcm"
    speed: float = 1.0
    language: str = "Auto"
    ref_audio: str | None = None
    ref_audio_path: str | None = None
    ref_text: str | None = None
    x_vector_only_mode: bool = False


class QwenVoiceService:
    def __init__(self, model_dir: Path, voice_dir: Path) -> None:
        self.model_dir = model_dir
        self.voice_dir = voice_dir
        self.voice_dir.mkdir(parents=True, exist_ok=True)
        self.model: Any = None
        self.generation_lock = threading.Lock()

    def load(self) -> None:
        if self.model is not None:
            return
        if not self.model_dir.exists():
            raise RuntimeError(f"Qwen model directory does not exist: {self.model_dir}")
        from qwen_tts import Qwen3TTSModel

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # RTX 40-series handles BF16 well; FP16 can produce NaN logits and a
        # CUDA device-side assert during Qwen's multi-codebook generation.
        dtype = torch.bfloat16 if device == "cuda:0" else torch.float32
        print(f"Loading Qwen3-TTS from {self.model_dir} on {device} ({dtype})", flush=True)
        self.model = Qwen3TTSModel.from_pretrained(
            str(self.model_dir), device_map=device, dtype=dtype
        )
        print("Qwen3-TTS ready", flush=True)

    def profiles(self) -> list[dict[str, Any]]:
        result = []
        for path in sorted(self.voice_dir.glob("*.json")):
            try:
                profile = json.loads(path.read_text(encoding="utf-8"))
                if Path(profile.get("path", "")).exists():
                    result.append(profile)
            except (OSError, ValueError):
                continue
        return result

    def profile(self, name: str) -> dict[str, Any] | None:
        return next((item for item in self.profiles() if item.get("name") == name), None)

    def synthesize(self, request: SpeechRequest) -> tuple[np.ndarray, int]:
        self.load()
        profile = self.profile(request.voice) if request.voice else None
        reference = request.ref_audio_path or request.ref_audio
        ref_text = request.ref_text
        if profile:
            reference = reference or profile["path"]
            ref_text = ref_text or profile.get("ref_text")
        if not reference:
            raise HTTPException(status_code=400, detail="A voice profile or reference audio is required")

        ref_path = Path(reference).expanduser()
        if not ref_path.is_absolute():
            ref_path = (ROOT / ref_path).resolve()
        if not ref_path.exists() or not ref_path.is_file():
            raise HTTPException(status_code=400, detail=f"Reference audio not found: {ref_path}")
        if not ref_text and not request.x_vector_only_mode:
            raise HTTPException(status_code=400, detail="ref_text is required unless x_vector_only_mode is true")

        kwargs: dict[str, Any] = {
            "text": request.input,
            "language": request.language,
            "ref_audio": str(ref_path),
        }
        if ref_text:
            kwargs["ref_text"] = ref_text
        if request.x_vector_only_mode:
            kwargs["x_vector_only_mode"] = True

        started = time.perf_counter()
        with self.generation_lock:
            wavs, sample_rate = self.model.generate_voice_clone(**kwargs)
        audio = np.asarray(wavs[0], dtype=np.float32)
        print(f"Generated {len(audio) / sample_rate:.2f}s in {time.perf_counter() - started:.2f}s", flush=True)
        return audio, int(sample_rate)


service: QwenVoiceService | None = None
app = FastAPI(title="Local Qwen3-TTS", version="0.1.0")


@app.get("/health")
def health() -> dict[str, Any]:
    assert service is not None
    return {"status": "ok", "model": str(service.model_dir), "loaded": service.model is not None,
            "cuda": torch.cuda.is_available(), "voices": len(service.profiles())}


@app.get("/v1/audio/voices")
def list_voices() -> dict[str, Any]:
    assert service is not None
    return {"voices": [], "uploaded_voices": service.profiles()}


@app.post("/v1/audio/voices")
async def upload_voice(
    audio_sample: UploadFile = File(...),
    name: str = Form(...),
    consent: str = Form(""),
    ref_text: str = Form(...),
    speaker_description: str = Form(""),
) -> dict[str, Any]:
    assert service is not None
    name = name.strip()
    ref_text = ref_text.strip()
    if not NAME_RE.fullmatch(name):
        raise HTTPException(status_code=400, detail="Voice name must use letters, numbers, _ or -")
    if not ref_text:
        raise HTTPException(status_code=400, detail="Reference transcript is required")
    suffix = Path(audio_sample.filename or ".wav").suffix.lower()
    if suffix not in {".wav", ".mp3", ".aac", ".m4a", ".flac", ".ogg"}:
        suffix = ".wav"
    output_path = service.voice_dir / f"{name}{suffix}"
    content = await audio_sample.read()
    if not content or len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Audio sample must be between 1 byte and 10 MB")
    output_path.write_bytes(content)
    profile = {"name": name, "path": str(output_path.resolve()), "ref_text": ref_text,
               "speaker_description": speaker_description.strip(), "consent": consent.strip(),
               "created_at": time.time()}
    (service.voice_dir / f"{name}.json").write_text(
        json.dumps(profile, ensure_ascii=True, indent=2), encoding="utf-8"
    )
    return profile


@app.delete("/v1/audio/voices/{name}")
def delete_voice(name: str) -> dict[str, str]:
    assert service is not None
    profile = service.profile(name)
    if not profile:
        raise HTTPException(status_code=404, detail="Voice not found")
    for path in (Path(profile["path"]), service.voice_dir / f"{name}.json"):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    return {"status": "deleted", "name": name}


@app.post("/v1/audio/speech")
def speech(request: SpeechRequest) -> Response:
    assert service is not None
    audio, sample_rate = service.synthesize(request)
    if request.response_format.lower() == "pcm":
        pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
        return Response(content=pcm, media_type="audio/pcm")
    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format="WAV", subtype="PCM_16")
    return Response(content=buffer.getvalue(), media_type="audio/wav")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--voice-dir", type=Path, default=DEFAULT_VOICE_DIR)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8091)
    args = parser.parse_args()
    global service
    service = QwenVoiceService(args.model_dir.resolve(), args.voice_dir.resolve())
    service.load()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
