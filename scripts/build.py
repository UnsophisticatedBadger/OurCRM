import shutil
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


def zip_windows_build() -> None:
    build_dir = ROOT / "dist" / "main.dist"
    (build_dir / "main.exe").rename(build_dir / "ourcrm.exe")
    package_dir = ROOT / "dist" / "ourcrm"
    build_dir.rename(package_dir)
    shutil.make_archive(str(ROOT / "dist" / "ourcrm-windows"), "zip", str(ROOT / "dist"), "ourcrm")
    shutil.rmtree(package_dir)


def main() -> None:
    subprocess.run([sys.executable, "-m", "nuitka", *get_nuitka_args()], check=True)
    if sys.platform == "win32":
        zip_windows_build()


if __name__ == "__main__":
    main()
