from pathlib import Path
import re

REQUIRED = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]

def grade(submission: Path, strict: bool = False) -> int:
    path = submission / "LOOP_CONTRACT.md"
    if not path.is_file():
        print("FAIL: missing LOOP_CONTRACT.md")
        return 2
    text = path.read_text(encoding="utf-8")
    if strict:
        text = re.sub(r"<!--.*?(?:-->|$)", "", text, flags=re.DOTALL)
        missing = [h for h in REQUIRED if not re.search(r"^" + re.escape(h) + r"[ \t]*$", text, re.MULTILINE)]
    else:
        missing = [h for h in REQUIRED if h not in text]
    if missing:
        print("FAIL: missing headings:")
        for heading in missing:
            print(f"  - {heading}")
        return 2
    if strict:
        empty = []
        for heading in REQUIRED:
            match = re.search(r"^" + re.escape(heading) + r"[ \t]*$", text, re.MULTILINE)
            body = text[match.end():]
            next_heading = re.search(r"^#{1,6}[ \t]+", body, re.MULTILINE)
            if next_heading:
                body = body[:next_heading.start()]
            if not body.strip():
                empty.append(heading)
        if empty:
            print("FAIL: empty sections:")
            for heading in empty:
                print(f"  - {heading}")
            return 2
    return 0
