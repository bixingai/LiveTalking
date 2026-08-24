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
