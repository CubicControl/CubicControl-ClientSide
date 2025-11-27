from __future__ import annotations

import datetime
from pathlib import Path
from typing import Optional


_STATE_FILE = Path(__file__).parent / ".last_manual_start"


def load_last_manual_start() -> Optional[datetime.datetime]:
    if not _STATE_FILE.exists():
        return None
    try:
        return datetime.datetime.fromisoformat(_STATE_FILE.read_text().strip())
    except ValueError:
        return None


def save_last_manual_start(timestamp: datetime.datetime) -> None:
    _STATE_FILE.write_text(timestamp.isoformat())