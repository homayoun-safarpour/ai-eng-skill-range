import json
from pathlib import Path

def grade(submission: Path) -> int:
    path = submission / "checkpoints.json"
    if not path.is_file():
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) < 2:
        return 2
    for row in data:
        if not row.get("name") or row.get("human_required") is not True:
            return 2
    return 0
