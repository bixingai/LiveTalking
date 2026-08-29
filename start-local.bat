@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
) else (
  set "PYTHON=python"
)

echo Starting LiveTalking on http://127.0.0.1:5555
set "LLM_PROVIDER=ollama"
set "OLLAMA_BASE_URL=http://127.0.0.1:11434"
set "OLLAMA_MODEL=ornith:latest"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "LIVETALKING_LOG=livetalking-local.log"
"%PYTHON%" app.py --transport webrtc --model wav2lip --avatar_id andy-wav2lip-256 --tts omnitts --TTS_SERVER http://127.0.0.1:8091 --REF_FILE andy-chinese-2 --listenport 5555
if errorlevel 1 pause
