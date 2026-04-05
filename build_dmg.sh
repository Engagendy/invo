#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="ULTRA_FORCE"
DIST_DIR="${ROOT_DIR}/dist"
APP_DIR="${DIST_DIR}/${APP_NAME}.app"
STAGE_DIR="${DIST_DIR}/dmg_stage"
RELEASE_VERSION="${RELEASE_VERSION:-$(python3 "${ROOT_DIR}/release_version.py" 2>/dev/null || true)}"

if [[ -z "${RELEASE_VERSION}" ]]; then
  RELEASE_VERSION="dev"
fi

DMG_BASENAME="${APP_NAME}-macos-${RELEASE_VERSION}"
DMG_PATH="${DIST_DIR}/${DMG_BASENAME}.dmg"

if [[ ! -d "${APP_DIR}" ]]; then
  echo "Missing ${APP_DIR}. Build the macOS app first with ./build_web_app.sh"
  exit 1
fi

rm -rf "${STAGE_DIR}"
mkdir -p "${STAGE_DIR}"
cp -R "${APP_DIR}" "${STAGE_DIR}/${APP_NAME}.app"
ln -s /Applications "${STAGE_DIR}/Applications"

rm -f "${DMG_PATH}"
hdiutil create \
  -volname "${APP_NAME}" \
  -srcfolder "${STAGE_DIR}" \
  -ov \
  -format UDZO \
  "${DMG_PATH}"

rm -rf "${STAGE_DIR}"
echo "DMG created: ${DMG_PATH}"
