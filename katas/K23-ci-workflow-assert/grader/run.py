from pathlib import Path

def grade(submission: Path) -> int:
    path = submission / ".github" / "workflows" / "ci.yml"
    if not path.is_file():
        return 2
    text = path.read_text(encoding="utf-8").casefold()
    if "jobs:" not in text or "pytest" not in text:
        return 2
    return 0
