# Audio8 TTS 0.1B

LiveTalking now includes a local Audio8 0.1B INT8 ONNX setup for low-memory CPU speech synthesis and zero-shot voice cloning.

## Installed components

- Model: `Audio8/audio8-TTS-0.1B-ONNX-INT8`
- Model files: `models/audio8-tts-0.1b-onnx-int8`
- Voice profiles: `models/audio8-tts-voices`
- Isolated environment: `.audio8-venv`
- HTTP service: `http://127.0.0.1:8024`
- Registered profile: `andy-chinese-2`

The runtime uses `CPUExecutionProvider`, so it does not compete with Wav2Lip or Ollama for GPU memory. Audio8 outputs 44.1 kHz PCM; the Audio8 LiveTalking launcher passes `--omni_tts_src_sr 44100` so LiveTalking resamples it correctly.

## Start

For the recommended one-click startup, run `start-all-local.bat`. It checks or starts Ollama, starts Audio8 TTS, waits for `/api/health`, then starts LiveTalking and waits for port `5555` before reporting readiness.

The services are separate because Audio8 is the TTS HTTP server on `8024`, while LiveTalking is the Avatar/WebRTC HTTP server on `5555`. The combined launcher opens each foreground service in its own window and keeps both windows available for diagnostics.

Manual startup remains available:

1. Run `start-audio8-tts.bat` and wait for `http://127.0.0.1:8024`.
2. Run `start-local-audio8.bat`.
3. Open `http://127.0.0.1:5555/index.html` and choose `Chat LLM` or `Echo 复读`.

Ollama must be running on `11434`, with `ornith:latest` available. The existing Qwen3-TTS launcher remains available when higher-fidelity Qwen output is preferred.

## Verification

```powershell
Invoke-RestMethod http://127.0.0.1:8024/api/health
curl.exe http://127.0.0.1:8024/v1/audio/speech `
  -H "Content-Type: application/json" `
  -d '{"model":"arktts-0.1b","input":"你好，这是本地语音测试。","voice":"andy-chinese-2","response_format":"wav"}' `
  -o models\audio8-andy-chinese-2-test.wav
```

The model is a preview release. Evaluate pronunciation and speaker similarity for each language before production use, and only clone voices with the speaker's consent.
