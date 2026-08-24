@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
) else (
  set "PYTHON=python"
)

echo Starting LiveTalking on http://127.0.0.1:5555
"%PYTHON%" app.py --transport webrtc --model wav2lip --avatar_id wav2lip256_avatar1 --listenport 5555
if errorlevel 1 pause
