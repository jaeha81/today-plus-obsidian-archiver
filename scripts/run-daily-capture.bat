@echo off
setlocal

cd /d "%~dp0.."

set "CHATGPT_URL=https://chatgpt.com/"

if "%~1"=="--help" (
    echo Usage: scripts\run-daily-capture.bat [--config "C:\path\config.yaml"]
    echo.
    echo Opens ChatGPT for manual capture, waits for you to copy Today Plus content,
    echo then archives the current clipboard through scripts\run-clipboard.bat.
    exit /b 0
)

echo Opening ChatGPT for manual Today Plus capture.
echo.
echo 1. Open Today Plus in ChatGPT.
echo 2. Select and copy the content you want to archive.
echo 3. Return to this window and press any key.
echo.
start "" "%CHATGPT_URL%"
pause

call scripts\run-clipboard.bat %*
exit /b %ERRORLEVEL%
