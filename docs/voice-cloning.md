# Voice Cloning Setup

LiveTalking separates speech recognition from voice cloning:

- FunASR/SenseVoice converts microphone audio to text through `/api/asr`.
- A clone-capable TTS engine generates speech from text using a reference voice.
- LiveTalking consumes that generated audio and performs lip-sync.

## Supported TTS adapters

The repository includes adapters for external clone-capable engines:

| Adapter | Start option | Reference inputs |
| --- | --- | --- |
| XTTS | `--tts xtts` | `--REF_FILE` reference audio; TTS server URL |
| GPT-SoVITS | `--tts gpt-sovits` | reference audio and transcript |
| CosyVoice | `--tts cosyvoice` | reference audio and transcript |
| IndexTTS2 | `--tts indextts2` | reference audio; Gradio server URL |

These adapters expect the corresponding TTS service and model to be installed separately. Installing FunASR does not install a voice-cloning model.

## Local Qwen3-TTS 0.6B Base

This repository includes a local adapter service for `Qwen/Qwen3-TTS-12Hz-0.6B-Base`. The model supports reference-audio voice cloning. Use a clean recording of a voice you own or have permission to use, and provide the exact transcript of that recording.

The model download is about 2.5 GB. The local service uses a separate `.qwen-tts-venv` so its pinned Transformers runtime does not replace LiveTalking's runtime. On CUDA, it uses BF16; this avoids the FP16 numerical failure that can trigger a CUDA device-side assert during multi-codebook generation on RTX cards.

### Install and download

```powershell
python -m venv --system-site-packages .qwen-tts-venv
.\.qwen-tts-venv\Scripts\python.exe -m pip install -r requirements-qwen3-tts.txt
.\.qwen-tts-venv\Scripts\python.exe -c "from modelscope import snapshot_download; print(snapshot_download('Qwen/Qwen3-TTS-12Hz-0.6B-Base', local_dir='models/qwen3-tts-0.6b-base'))"
```

### Start the service

Run `start-qwen3-tts.bat`, or use:

```powershell
.\.qwen-tts-venv\Scripts\python.exe tools\qwen3_tts_server.py --port 8091
```

Verify `http://127.0.0.1:8091/health` reports `"cuda": true` and `"loaded": true`.

### Create and use a voice profile

The existing `/tts/index.html` page can upload a reference recording. Set its server URL to `http://127.0.0.1:8091`, enter a profile name and exact transcript, then upload. The service stores the profile under the ignored `models/qwen3-tts-voices/` directory.

For a command-line test:

```powershell
curl.exe -X POST http://127.0.0.1:8091/v1/audio/voices `
  -F "audio_sample=@C:\path\to\reference.wav" `
  -F "name=my_voice" `
  -F "consent=confirmed" `
  -F "ref_text=Exact transcript of the reference recording"
```

Then launch LiveTalking with `start-local-qwen3-tts.bat`. It uses the `qwen-demo` profile by default; edit `QWEN_VOICE` in that batch file to match your uploaded profile name. The companion `start-local.bat` remains the default LiveTalking launcher.

The speech endpoint also supports direct local testing with JSON fields `input`, `voice`, `response_format`, `language`, `ref_audio_path`, and `ref_text`. `response_format: "pcm"` is the format consumed by the LiveTalking `omnitts` adapter; `wav` is convenient for inspecting a generated file.

## Example: GPT-SoVITS-compatible service

Start the compatible TTS service first, then launch LiveTalking with a clean reference recording and its exact transcript:

```powershell
python app.py --transport webrtc --model wav2lip `
  --tts gpt-sovits `
  --TTS_SERVER http://127.0.0.1:9880 `
  --REF_FILE C:\path\to\voice-reference.wav `
  --REF_TEXT "Exact transcript of the reference recording" `
  --listenport 5555
```

Use a short, clean, single-speaker recording with minimal background noise. Only clone voices you own or have permission to use.

## FunASR local endpoint

After restarting LiveTalking with FunASR installed, the server registers `GET /api/asr` as a WebSocket endpoint. The first recognition request downloads the SenseVoiceSmall and VAD models through ModelScope, then uses CUDA when available.

The existing browser ASR page can auto-detect this endpoint at `/asr/index.html`. Text-driven TTS and avatar playback do not depend on FunASR.
