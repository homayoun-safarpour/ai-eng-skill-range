import re
from pathlib import Path


def _strip_comment(line: str) -> str:
    if line.lstrip().startswith("#"):
        return ""
    return re.sub(r"\s#.*$", "", line).rstrip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _runs_pytest(lines: list[str]) -> bool:
    """True when a `run:` step under `steps:` calls pytest (one line or a block)."""
    in_steps = False
    steps_indent = 0
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if in_steps and _indent(line) <= steps_indent and not line.lstrip().startswith("-"):
            in_steps = False
        if re.match(r"\s*steps:\s*$", line):
            in_steps, steps_indent = True, _indent(line)
            continue
        if not in_steps:
            continue
        match = re.match(r"(\s*(?:-\s+)?)run:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(2)
        if value[:1] in ("|", ">"):
            key_indent = len(match.group(1))
            body = []
            for nxt in lines[i + 1 :]:
                if nxt.strip() and _indent(nxt) <= key_indent:
                    break
                body.append(nxt)
            value = "\n".join(body)
        if re.search(r"\bpytest\b", value):
            return True
    return False


def grade(submission: Path) -> int:
    path = submission / ".github" / "workflows" / "ci.yml"
    if not path.is_file():
        print("FAIL: missing .github/workflows/ci.yml")
        return 2
    lines = [_strip_comment(line) for line in path.read_text(encoding="utf-8").casefold().splitlines()]
    if not any(re.match(r"jobs:", line) for line in lines):
        print("FAIL: no top-level jobs: key")
        return 2
    if not _runs_pytest(lines):
        print("FAIL: no run: step under steps: calls pytest")
        return 2
    return 0
