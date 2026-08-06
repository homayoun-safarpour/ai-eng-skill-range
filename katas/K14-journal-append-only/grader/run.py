from pathlib import Path

def grade(submission: Path) -> int:
    path = submission / "JOURNAL.md"
    if not path.is_file():
        return 2
    text = path.read_text(encoding="utf-8").casefold()
    if "gates:" not in text or "decision:" not in text:
        return 2
    return 0
