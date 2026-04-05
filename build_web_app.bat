@echo off
setlocal

set "APP_NAME=ULTRA_FORCE"
set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv-web-build"
set "DIST_DIR=%ROOT_DIR%dist"
set "APP_DIR=%DIST_DIR%\%APP_NAME%"
if "%TROCR_MODEL_NAME%"=="" set "TROCR_MODEL_NAME=microsoft/trocr-base-handwritten"
if "%FAST_RELEASE%"=="" set "FAST_RELEASE=0"
set "REQ_FINGERPRINT_FILE=%VENV_DIR%\.requirements-fingerprint"

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

for %%I in ("%FAST_RELEASE%") do set "FAST_RELEASE=%%~I"

for /f "usebackq delims=" %%H in (`powershell -NoProfile -Command "$content = (Get-Content '%ROOT_DIR%requirements-ai.txt' -Raw) + (Get-Content '%ROOT_DIR%requirements-web.txt' -Raw) + '%TROCR_MODEL_NAME%' + '%FAST_RELEASE%' + 'Windows'; $hash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($content))).Replace('-', '').ToLower(); Write-Output $hash"`) do set "CURRENT_FINGERPRINT=%%H"
set "PREVIOUS_FINGERPRINT="
if exist "%REQ_FINGERPRINT_FILE%" set /p PREVIOUS_FINGERPRINT=<"%REQ_FINGERPRINT_FILE%"

if /I not "%CURRENT_FINGERPRINT%"=="%PREVIOUS_FINGERPRINT%" (
  python -m pip install --upgrade pip
  python -m pip install -r "%ROOT_DIR%requirements-ai.txt"
  python -m pip install -r "%ROOT_DIR%requirements-web.txt"
  python -m pip install paddlepaddle==3.2.0 PyYAML==6.0.2
  python -m pip install pyinstaller
  >"%REQ_FINGERPRINT_FILE%" echo %CURRENT_FINGERPRINT%
) else (
  echo Reusing cached build environment
)

python -c "from pathlib import Path; from transformers import TrOCRProcessor, VisionEncoderDecoderModel; model=r'%TROCR_MODEL_NAME%'; normalized=model.replace('/', '--'); export_dir=Path(r'%ROOT_DIR%')/'.build-trocr-export'/normalized; export_dir.mkdir(parents=True, exist_ok=True); existing=(export_dir/'config.json').exists() and (export_dir/'model.safetensors').exists(); print('Reusing exported TrOCR model' if existing else 'Exporting TrOCR model'); trocr_processor=TrOCRProcessor.from_pretrained(model); trocr_model=VisionEncoderDecoderModel.from_pretrained(model, use_safetensors=True); trocr_processor.save_pretrained(export_dir); trocr_model.save_pretrained(export_dir, safe_serialization=True)"

if /I "%FAST_RELEASE%"=="1" (
  echo FAST_RELEASE enabled: reusing PyInstaller build cache
  pyinstaller ^
    --noconfirm ^
    --name "%APP_NAME%" ^
    --onedir ^
    --collect-all paddleocr ^
    --collect-all rapidocr_onnxruntime ^
    --hidden-import paddleocr ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import transformers.models.trocr.processing_trocr ^
    --hidden-import transformers.models.trocr.modeling_trocr ^
    --hidden-import transformers.models.vision_encoder_decoder.modeling_vision_encoder_decoder ^
    --hidden-import tokenizers ^
    --hidden-import sentencepiece ^
    --hidden-import safetensors ^
    "%ROOT_DIR%web_app.py"
) else (
  pyinstaller ^
    --noconfirm ^
    --clean ^
    --name "%APP_NAME%" ^
    --onedir ^
    --collect-all paddleocr ^
    --collect-all rapidocr_onnxruntime ^
    --hidden-import paddleocr ^
    --hidden-import torch ^
    --hidden-import transformers ^
    --hidden-import transformers.models.trocr.processing_trocr ^
    --hidden-import transformers.models.trocr.modeling_trocr ^
    --hidden-import transformers.models.vision_encoder_decoder.modeling_vision_encoder_decoder ^
    --hidden-import tokenizers ^
    --hidden-import sentencepiece ^
    --hidden-import safetensors ^
    "%ROOT_DIR%web_app.py"
)

if exist "%APP_DIR%\web" rmdir /S /Q "%APP_DIR%\web"
xcopy /E /I /Y "%ROOT_DIR%web" "%APP_DIR%\web\" >nul
if not exist "%APP_DIR%\models" mkdir "%APP_DIR%\models"
if not exist "%APP_DIR%\source" mkdir "%APP_DIR%\source"
if not exist "%APP_DIR%\processed" mkdir "%APP_DIR%\processed"
if not exist "%APP_DIR%\debug_images" mkdir "%APP_DIR%\debug_images"
if exist "%ROOT_DIR%models" xcopy /E /I /Y "%ROOT_DIR%models" "%APP_DIR%\models\" >nul
if exist "%USERPROFILE%\.paddlex\official_models" xcopy /E /I /Y "%USERPROFILE%\.paddlex\official_models" "%APP_DIR%\models\official_models\" >nul
set "TROCR_EXPORT_DIR=%ROOT_DIR%.build-trocr-export\%TROCR_MODEL_NAME:/=--%"
if exist "%TROCR_EXPORT_DIR%" xcopy /E /I /Y "%TROCR_EXPORT_DIR%" "%APP_DIR%\models\trocr\%TROCR_MODEL_NAME:/=--%\" >nul

echo Build completed: %APP_DIR%
endlocal
