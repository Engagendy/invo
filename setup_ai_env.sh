#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv311"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Python 3.11 not found. Set PYTHON_BIN or install python3.11 first."
  exit 1
fi

"${PYTHON_BIN}" -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "${ROOT_DIR}/requirements-ai.txt"

OS_NAME="$(uname -s)"
if [[ "${OS_NAME}" == "Darwin" ]]; then
  python -m pip install "numpy==1.26.4" "paddlepaddle==3.0.0" "PyYAML==6.0.2"
else
  python -m pip install "paddlepaddle==3.2.0"
fi

echo
echo "AI environment ready at ${VENV_DIR}"
echo "Activate with: source ${VENV_DIR}/bin/activate"
