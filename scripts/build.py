import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _data_file_arg(source: Path, dest: str) -> str:
    return f"--include-data-files={source}={dest}"


def get_nuitka_args() -> list[str]:
    # --include-data-dir won't bundle these: Nuitka 1.4+ deliberately excludes
    # *.py/*.mako from it, treating them as code rather than data. Alembic
    # loads env.py/script.py.mako/versions/*.py via its own file-path lookups
    # at runtime though, not Python's import system, so they must be listed
    # explicitly via --include-data-files or a packaged build can't open a
    # database at all. The versions/*.py pattern picks up future migrations
    # automatically — no need to update this file when a new one is added.
    migrations_src = ROOT / "src" / "ourcrm" / "database" / "migrations"
    args = [
        "--standalone",
        "--enable-plugin=pyside6",
        f"--output-dir={ROOT / 'dist'}",
        _data_file_arg(migrations_src / "env.py", "ourcrm/database/migrations/env.py"),
        _data_file_arg(
            migrations_src / "script.py.mako", "ourcrm/database/migrations/script.py.mako"
        ),
        _data_file_arg(
            migrations_src / "versions" / "*.py", "ourcrm/database/migrations/versions/"
        ),
        # env.py is bundled as opaque data, not compiled code, so Nuitka's
        # static import analysis never sees its `from logging.config import
        # fileConfig`. Nothing else in the app imports logging, so it must be
        # forced in explicitly or a packaged build fails the first time it
        # opens a database.
        "--include-module=logging.config",
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
