@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
) else (
  set "PYTHON=python"
)

set "QWEN_TTS_SERVER=http://127.0.0.1:8091"
set "QWEN_VOICE=qwen-demo"
echo Starting LiveTalking with Qwen3-TTS voice %QWEN_VOICE% on http://127.0.0.1:5555
"%PYTHON%" app.py --transport webrtc --model wav2lip --avatar_id wav2lip256_avatar1 --tts omnitts --TTS_SERVER %QWEN_TTS_SERVER% --REF_FILE %QWEN_VOICE% --listenport 5555
if errorlevel 1 pause
