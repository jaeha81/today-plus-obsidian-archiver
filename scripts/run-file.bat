@echo off
setlocal

cd /d "%~dp0.."

if "%~1"=="" (
    echo Usage: scripts\run-file.bat "C:\path\to\today_plus.html" [--config "C:\path\config.yaml"]
    exit /b 2
)

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

if "%~1"=="--help" (
    "%PYTHON_EXE%" main.py --help
    exit /b %ERRORLEVEL%
)

"%PYTHON_EXE%" main.py --file "%~1" %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%
