#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="ULTRA_FORCE"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"
VENV_DIR="${ROOT_DIR}/.venv-web-build"
DIST_DIR="${ROOT_DIR}/dist"
APP_DIR="${DIST_DIR}/${APP_NAME}"
OS_NAME="$(uname -s)"
MAC_BUILD_ARCH="${MAC_BUILD_ARCH:-auto}"
TROCR_MODEL_NAME="${TROCR_MODEL_NAME:-microsoft/trocr-base-handwritten}"

copy_trocr_cache() {
  local destination_base="$1"
  local normalized_model="${TROCR_MODEL_NAME//\//--}"
  local candidate_dirs=(
    "${HOME}/.cache/huggingface/hub/models--${normalized_model}"
    "${HOME}/Library/Caches/huggingface/hub/models--${normalized_model}"
  )

  mkdir -p "${destination_base}/huggingface/hub"
  for candidate in "${candidate_dirs[@]}"; do
    if [[ -d "${candidate}" ]]; then
      rsync -a "${candidate}" "${destination_base}/huggingface/hub/"
      return
    fi
  done
}

resolve_python_cmd() {
  if [[ "${OS_NAME}" != "Darwin" ]]; then
    echo "${PYTHON_BIN}"
    return
  fi

  if [[ "${MAC_BUILD_ARCH}" == "arm64" || "${MAC_BUILD_ARCH}" == "auto" ]]; then
    if [[ -x "/opt/homebrew/bin/python3.11" ]]; then
      echo "arch -arm64 /opt/homebrew/bin/python3.11"
      return
    fi
  fi

  echo "${PYTHON_BIN}"
}

PYTHON_CMD="$(resolve_python_cmd)"
BUILD_MACHINE="$(uname -m)"

if ! eval "${PYTHON_CMD} -V" >/dev/null 2>&1; then
  echo "Python 3.11 not found for the requested build mode."
  if [[ "${OS_NAME}" == "Darwin" && "${MAC_BUILD_ARCH}" == "arm64" ]]; then
    echo "Install native Apple Silicon Python 3.11 under /opt/homebrew and rerun."
  fi
  exit 1
fi

if [[ "${OS_NAME}" == "Darwin" ]]; then
  echo "Host machine architecture: ${BUILD_MACHINE}"
  echo "Requested macOS build arch: ${MAC_BUILD_ARCH}"
  echo "Using Python command: ${PYTHON_CMD}"
fi

eval "${PYTHON_CMD} -m venv \"${VENV_DIR}\""
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "${ROOT_DIR}/requirements-ai.txt"
python -m pip install -r "${ROOT_DIR}/requirements-web.txt"
if [[ "${OS_NAME}" == "Darwin" ]]; then
  python -m pip install "numpy==1.26.4" "paddlepaddle==3.0.0" "PyYAML==6.0.2"
else
  python -m pip install "paddlepaddle==3.2.0" "PyYAML==6.0.2"
fi
python -m pip install pyinstaller

python -c "from transformers import TrOCRProcessor, VisionEncoderDecoderModel; model='${TROCR_MODEL_NAME}'; TrOCRProcessor.from_pretrained(model); VisionEncoderDecoderModel.from_pretrained(model, use_safetensors=True)"

if [[ "${OS_NAME}" == "Darwin" ]]; then
  pyinstaller \
    --noconfirm \
    --clean \
    --name "${APP_NAME}" \
    --windowed \
    --osx-bundle-identifier "com.ultraforce.ocr" \
    --target-arch "${MAC_BUILD_ARCH}" \
    --collect-all paddleocr \
    --collect-all rapidocr_onnxruntime \
    --hidden-import paddleocr \
    --hidden-import torch \
    --hidden-import transformers \
    --hidden-import transformers.models.trocr.processing_trocr \
    --hidden-import transformers.models.trocr.modeling_trocr \
    --hidden-import transformers.models.vision_encoder_decoder.modeling_vision_encoder_decoder \
    --hidden-import tokenizers \
    --hidden-import sentencepiece \
    --hidden-import safetensors \
    "${ROOT_DIR}/web_app.py"
  APP_DIR="${DIST_DIR}/${APP_NAME}.app/Contents/MacOS"
else
  pyinstaller \
    --noconfirm \
    --clean \
    --name "${APP_NAME}" \
    --onedir \
    --collect-all paddleocr \
    --collect-all rapidocr_onnxruntime \
    --hidden-import paddleocr \
    --hidden-import torch \
    --hidden-import transformers \
    --hidden-import transformers.models.trocr.processing_trocr \
    --hidden-import transformers.models.trocr.modeling_trocr \
    --hidden-import transformers.models.vision_encoder_decoder.modeling_vision_encoder_decoder \
    --hidden-import tokenizers \
    --hidden-import sentencepiece \
    --hidden-import safetensors \
    "${ROOT_DIR}/web_app.py"
fi

mkdir -p "${APP_DIR}/web"
mkdir -p "${APP_DIR}/models"
mkdir -p "${APP_DIR}/source"
mkdir -p "${APP_DIR}/processed"
mkdir -p "${APP_DIR}/debug_images"

rm -rf "${APP_DIR}/web"
cp -R "${ROOT_DIR}/web" "${APP_DIR}/web"

if [[ -d "${ROOT_DIR}/models" ]]; then
  rsync -a "${ROOT_DIR}/models/" "${APP_DIR}/models/"
fi

if [[ -d "${HOME}/.paddlex/official_models" ]]; then
  mkdir -p "${APP_DIR}/models/official_models"
  rsync -a "${HOME}/.paddlex/official_models/" "${APP_DIR}/models/official_models/"
fi

copy_trocr_cache "${APP_DIR}/models"

echo "Build completed: ${APP_DIR}"
