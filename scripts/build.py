import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def get_nuitka_args() -> list[str]:
    args = [
        "--standalone",
        "--enable-plugin=pyside6",
        f"--output-dir={ROOT / 'dist'}",
    ]
    if sys.platform == "win32":
        args.append("--windows-console-mode=disable")
        args.append("--assume-yes-for-downloads")
    args.append(str(ROOT / "src" / "ourcrm" / "main.py"))
    return args


def main() -> None:
    subprocess.run([sys.executable, "-m", "nuitka", *get_nuitka_args()], check=True)


if __name__ == "__main__":
    main()
