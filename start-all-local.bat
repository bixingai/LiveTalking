@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==============================================
echo LiveTalking local startup
echo Order: Ollama ^> Audio8 TTS ^> LiveTalking
echo ==============================================

call :wait_port 11434 5
if errorlevel 1 (
  echo Ollama is not listening. Starting ollama serve...
  start "Ollama" /min cmd /c "ollama serve"
  call :wait_port 11434 60
  if errorlevel 1 goto :startup_failed
)
echo [OK] Ollama is ready on 11434

call :wait_http 8024 "/api/health" 2
if errorlevel 1 (
  echo Starting Audio8 TTS...
  start "Audio8 TTS" cmd /k call "%~dp0start-audio8-tts.bat"
  call :wait_http 8024 "/api/health" 120
  if errorlevel 1 goto :startup_failed
)
echo [OK] Audio8 TTS is ready on 8024

call :wait_port 5555 2
if not errorlevel 1 (
  echo LiveTalking is already listening on 5555.
  goto :ready
)
echo Starting LiveTalking...
start "LiveTalking" cmd /k call "%~dp0start-local-audio8.bat"
call :wait_port 5555 180
if errorlevel 1 goto :startup_failed

:ready
echo.
echo [READY] Open http://127.0.0.1:5555/index.html
echo Keep the Audio8 and LiveTalking windows open while using the app.
exit /b 0

:wait_port
set "WAIT_PORT=%~1"
set /a WAIT_SECONDS=%~2
:wait_port_loop
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "$x=Get-NetTCPConnection -LocalPort %WAIT_PORT% -State Listen -ErrorAction SilentlyContinue; if($x){'ready'}"`) do if "%%A"=="ready" exit /b 0
if %WAIT_SECONDS% LEQ 0 exit /b 1
timeout /t 1 /nobreak >nul
set /a WAIT_SECONDS-=1
goto :wait_port_loop

:wait_http
set "WAIT_HTTP_PORT=%~1"
set "WAIT_HTTP_PATH=%~2"
set /a WAIT_SECONDS=%~3
:wait_http_loop
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "try{$r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:%WAIT_HTTP_PORT%%WAIT_HTTP_PATH%' -TimeoutSec 3;if($r.StatusCode -eq 200){'ready'}}catch{}"`) do if "%%A"=="ready" exit /b 0
if %WAIT_SECONDS% LEQ 0 exit /b 1
timeout /t 1 /nobreak >nul
set /a WAIT_SECONDS-=1
goto :wait_http_loop

:startup_failed
echo.
echo [FAILED] A required service did not become ready.
echo Check the open service window for the exact model or dependency error.
pause
exit /b 1
