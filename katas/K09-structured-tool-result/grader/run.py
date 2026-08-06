import json
from pathlib import Path

def grade(submission: Path) -> int:
    path = submission / "result.json"
    if not path.is_file():
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("tool") or not data.get("args_hash"):
        return 2
    if data.get("status") not in {"ok", "error"}:
        return 2
    return 0
