#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELEASE_VERSION="${RELEASE_VERSION:-$(python3 "${ROOT_DIR}/release_version.py")}"
DMG_NAME="ULTRA_FORCE-macos-${RELEASE_VERSION}.dmg"
CHECKSUM_NAME="ULTRA_FORCE-macos-${RELEASE_VERSION}-sha256.txt"

if [[ "$(uname -s)" == "Darwin" && "${MAC_BUILD_ARCH:-auto}" == "auto" ]]; then
  if [[ -x "/opt/homebrew/bin/python3.11" ]]; then
    export MAC_BUILD_ARCH="arm64"
  fi
fi

bash "${ROOT_DIR}/build_web_app.sh"
bash "${ROOT_DIR}/build_dmg.sh"
shasum -a 256 "${ROOT_DIR}/dist/${DMG_NAME}" > "${ROOT_DIR}/dist/${CHECKSUM_NAME}"

echo
echo "Release ready:"
echo "  ${ROOT_DIR}/dist/${DMG_NAME}"
echo "  ${ROOT_DIR}/dist/${CHECKSUM_NAME}"
