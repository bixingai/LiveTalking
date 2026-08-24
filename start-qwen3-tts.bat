@echo off
setlocal
cd /d "%~dp0"

if not exist ".qwen-tts-venv\Scripts\python.exe" (
  echo Missing .qwen-tts-venv. Run the Qwen3-TTS setup commands in docs\voice-cloning.md first.
  pause
  exit /b 1
)

echo Starting local Qwen3-TTS on http://127.0.0.1:8091
".qwen-tts-venv\Scripts\python.exe" tools\qwen3_tts_server.py --port 8091
if errorlevel 1 pause
