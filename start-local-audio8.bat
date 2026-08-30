@echo off
setlocal
cd /d "%~dp0"
set "NUMBA_CACHE_DIR=%TEMP%\livetalking-numba-cache"
if not exist "%NUMBA_CACHE_DIR%" mkdir "%NUMBA_CACHE_DIR%"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
) else (
  set "PYTHON=python"
)

set "LLM_PROVIDER=ollama"
set "OLLAMA_BASE_URL=http://127.0.0.1:11434"
set "OLLAMA_MODEL=ornith:latest"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "LIVETALKING_LOG=livetalking-audio8.log"
echo Starting LiveTalking with Audio8 voice andy-chinese-2 on http://127.0.0.1:5555
"%PYTHON%" app.py --transport webrtc --model wav2lip --avatar_id andy-wav2lip-256 --tts omnitts --TTS_SERVER http://127.0.0.1:8024 --REF_FILE andy-chinese-2 --omni_tts_src_sr 44100 --listenport 5555
if errorlevel 1 pause
