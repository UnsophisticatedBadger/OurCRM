import platform
import traceback
from datetime import UTC, datetime
from pathlib import Path
from types import TracebackType

from ourcrm.core.app_version import app_version


def format_crash_entry(
    exc_type: type[BaseException], exc_value: BaseException, exc_tb: TracebackType | None
) -> str:
    timestamp = datetime.now(UTC).isoformat()
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    return f"--- {timestamp} | OurCRM {app_version()} | {platform.platform()} ---\n{tb_text}\n"


def write_crash_log(data_dir: Path, entry: str) -> Path:
    log_path = data_dir / "logs" / "crash.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)
    return log_path
