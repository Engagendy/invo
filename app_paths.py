import os
import sys
from pathlib import Path


APP_DIR_NAME = "ULTRA_FORCE"


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def runtime_root() -> Path:
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def user_data_root() -> Path:
    override = os.environ.get("ULTRA_FORCE_HOME", "").strip()
    if override:
        path = Path(override).expanduser().resolve()
    elif sys.platform == "win32":
        path = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / APP_DIR_NAME
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / APP_DIR_NAME
    else:
        path = Path.home() / ".ultra_force"
    path.mkdir(parents=True, exist_ok=True)
    return path


def bundled_web_dir() -> Path:
    return runtime_root() / "web"


def bundled_models_dir() -> Path:
    return runtime_root() / "models"
