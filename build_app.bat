@echo off
setlocal

set "APP_NAME=InvoiceProcessor"
set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv-build"
set "DIST_DIR=%ROOT_DIR%dist"

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 first.
  exit /b 1
)

py -3.11 -V >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 is not installed.
  echo Install it, then rerun this script.
  exit /b 1
)

if not exist "%VENV_DIR%" (
  py -3.11 -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip
python -m pip install -r "%ROOT_DIR%requirements.txt"
python -m pip install pyinstaller

pyinstaller ^
  --noconfirm ^
  --clean ^
  --name "%APP_NAME%" ^
  --onedir ^
  --collect-all paddleocr ^
  --hidden-import paddleocr ^
  "%ROOT_DIR%invoice_processor.py"

if not exist "%DIST_DIR%\%APP_NAME%\source" mkdir "%DIST_DIR%\%APP_NAME%\source"
if not exist "%DIST_DIR%\%APP_NAME%\processed" mkdir "%DIST_DIR%\%APP_NAME%\processed"
if not exist "%DIST_DIR%\%APP_NAME%\models" mkdir "%DIST_DIR%\%APP_NAME%\models"
if exist "%USERPROFILE%\.paddlex\official_models" xcopy /E /I /Y "%USERPROFILE%\.paddlex\official_models" "%DIST_DIR%\%APP_NAME%\models\official_models\" >nul
if exist "%ROOT_DIR%2026-04-03_102980.pdf" copy /Y "%ROOT_DIR%2026-04-03_102980.pdf" "%DIST_DIR%\%APP_NAME%\source\" >nul

echo Build completed: %DIST_DIR%\%APP_NAME%
endlocal
