import json
from pathlib import Path

KEYS = ("goal", "max_turns", "budget", "no_progress")

def grade(submission: Path) -> int:
    path = submission / "stop_layers.json"
    if not path.is_file():
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    for k in KEYS:
        if not str(data.get(k) or "").strip():
            return 2
    return 0
