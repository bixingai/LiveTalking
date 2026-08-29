@echo off
setlocal
cd /d "%~dp0"

if not exist ".audio8-venv\Scripts\python.exe" (
  echo Missing .audio8-venv. Follow docs\audio8-tts.md first.
  pause
  exit /b 1
)

set "ARKTTS_MODEL_DIR=%CD%\models\audio8-tts-0.1b-onnx-int8"
set "ARKTTS_VOICES_DIR=%CD%\models\audio8-tts-voices"
set "ARKTTS_THREADS=5"
echo Starting Audio8 TTS on http://127.0.0.1:8024
pushd ".downloads\Audio8_TTS\onnx_runtime_0_1b_int8"
"%CD%\..\..\..\.audio8-venv\Scripts\python.exe" -m uvicorn arktts_runtime.service:app --host 127.0.0.1 --port 8024
popd
if errorlevel 1 pause
