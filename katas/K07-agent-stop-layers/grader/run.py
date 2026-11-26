import json
from pathlib import Path

KEYS = ("goal", "max_turns", "budget", "no_progress")

def grade(submission: Path) -> int:
    path = submission / "stop_layers.json"
    if not path.is_file():
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return 2
    for k in KEYS:
        value = data.get(k)
        if not isinstance(value, str) or not value.strip():
            return 2
    return 0
