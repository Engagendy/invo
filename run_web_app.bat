@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
  echo Missing %VENV_DIR%. Create it and install requirements-normal.txt and requirements-web.txt first.
  exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python "%ROOT_DIR%web_app.py"
