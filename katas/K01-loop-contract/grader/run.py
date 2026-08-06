from pathlib import Path

REQUIRED = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]

def grade(submission: Path) -> int:
    path = submission / "LOOP_CONTRACT.md"
    if not path.is_file():
        return 2
    text = path.read_text(encoding="utf-8")
    return 0 if all(h in text for h in REQUIRED) else 2
