@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv311"

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 first.
  exit /b 1
)

py -3.11 -V >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 is not installed.
  exit /b 1
)

if not exist "%VENV_DIR%" (
  py -3.11 -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip
python -m pip install -r "%ROOT_DIR%requirements-ai.txt"
python -m pip install paddlepaddle==3.2.0 PyYAML==6.0.2

echo.
echo AI environment ready at %VENV_DIR%
endlocal
