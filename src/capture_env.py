import sys
import json
import platform
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
METADATA_DIR.mkdir(parents=True, exist_ok=True)

ENV_INFO_PATH = METADATA_DIR / "env_info.json"


def main():
    print("[capture_env] ROOT:", ROOT)
    print("[capture_env] Writing to:", ENV_INFO_PATH)

    libs_to_check = ["pandas", "numpy", "yaml", "sklearn"]

    libs = {}
    for name in libs_to_check:
        try:
            module = importlib.import_module(name)
            libs[name] = getattr(module, "__version__", "unknown")
        except ImportError:
            libs[name] = "not installed"

    env_info = {
        "python": sys.version,
        "os": platform.platform(),
        "libraries": libs,
    }

    with ENV_INFO_PATH.open("w", encoding="utf-8") as f:
        json.dump(env_info, f, indent=4)

    print("[capture_env] Done.")


if __name__ == "__main__":
    main()
