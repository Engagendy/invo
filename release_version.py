import os
import subprocess
from pathlib import Path


def detect_release_version(root_dir: Path) -> str:
    explicit = os.environ.get("RELEASE_VERSION", "").strip()
    if explicit:
        return explicit

    github_ref_name = os.environ.get("GITHUB_REF_NAME", "").strip()
    if github_ref_name:
        return github_ref_name

    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match"],
            cwd=root_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        tag = result.stdout.strip()
        if tag:
            return tag
    except Exception:
        pass

    return "dev"


if __name__ == "__main__":
    print(detect_release_version(Path(__file__).resolve().parent))
