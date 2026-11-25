import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_S = 10

# The grader holds its own cases. Any status.json in the submission is ignored:
# a submission must never choose the answer it is graded against.
# Each case: (label, status.json text or None for a missing file, expected exit code).
CASES = [
    ("ok is true", '{"ok": true}', 0),
    ("ok is false", '{"ok": false}', 2),
    ("status.json is missing", None, 2),
    ('ok is "yes" (not a bool)', '{"ok": "yes"}', 2),
]


def _run_case(submission: Path, status: str | None) -> int | None:
    with tempfile.TemporaryDirectory(prefix="k02_") as tmp:
        work = Path(tmp) / "sub"
        shutil.copytree(submission, work)
        target = work / "status.json"
        if target.exists():
            target.unlink()
        if status is not None:
            target.write_text(status, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(work / "gate.py")],
                cwd=work,
                capture_output=True,
                check=False,
                text=True,
                timeout=TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return None
        return proc.returncode


def grade(submission: Path) -> int:
    if not (submission / "gate.py").is_file():
        print("FAIL: missing gate.py")
        return 2
    for label, status, expected in CASES:
        code = _run_case(submission, status)
        if code is None:
            print(f"FAIL: gate.py did not finish within {TIMEOUT_S} s when {label}")
            return 2
        if code != expected:
            print(f"FAIL: when {label}, gate.py exited {code}; expected {expected}")
            return 2
    return 0
