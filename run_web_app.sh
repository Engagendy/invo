#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  echo "Missing ${VENV_DIR}. Create it and install requirements-normal.txt and requirements-web.txt first."
  exit 1
fi

source "${VENV_DIR}/bin/activate"
python "${ROOT_DIR}/web_app.py"
