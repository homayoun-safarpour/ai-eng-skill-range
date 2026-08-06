import json
import subprocess
import sys
from pathlib import Path

def grade(submission: Path) -> int:
    gate = submission / "gate.py"
    status = submission / "status.json"
    if not gate.is_file() or not status.is_file():
        return 2
    # run with cwd=submission so relative status works; also patch for __file__ style
    proc = subprocess.run([sys.executable, str(gate)], cwd=submission, capture_output=True, text=True)
    data = json.loads(status.read_text(encoding="utf-8"))
    expect = 0 if data.get("ok") else 2
    return 0 if proc.returncode == expect else 2
