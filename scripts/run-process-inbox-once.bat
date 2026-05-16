@echo off
setlocal

cd /d "%~dp0.."

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

rem Optional: pass --archive-processed to move handled source files into inbox\processed.

if "%~1"=="--help" (
    "%PYTHON_EXE%" main.py --help
    exit /b %ERRORLEVEL%
)

"%PYTHON_EXE%" main.py --process-inbox-once %*
exit /b %ERRORLEVEL%
