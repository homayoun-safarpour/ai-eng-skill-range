import re
from pathlib import Path

REQUIRED = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]


def _sections(text: str) -> dict[str, list[str]]:
    """Map each heading line to the lines under it.

    HTML comments are removed first, and lines inside fenced code blocks are never
    read as headings, so a heading only counts when a reader of the page sees it.
    """
    text = re.sub(r"<!--.*?(-->|\Z)", "", text, flags=re.DOTALL)
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"#{1,2}\s", stripped):
            current = sections.setdefault(stripped, [])
            continue
        if current is not None:
            current.append(stripped)
    return sections


def _find(sections: dict[str, list[str]], heading: str) -> list[str] | None:
    for name, body in sections.items():
        if name == heading or name.startswith(heading + " "):
            return body
    return None


def grade(submission: Path) -> int:
    path = submission / "LOOP_CONTRACT.md"
    if not path.is_file():
        print("FAIL: missing LOOP_CONTRACT.md")
        return 2
    sections = _sections(path.read_text(encoding="utf-8"))
    missing = [h for h in REQUIRED if _find(sections, h) is None]
    if missing:
        print("FAIL: missing headings:")
        for heading in missing:
            print(f"  - {heading}")
        return 2
    empty = [h for h in REQUIRED if not any(_find(sections, h))]
    if empty:
        print("FAIL: empty headings (no text under them):")
        for heading in empty:
            print(f"  - {heading}")
        return 2
    return 0
