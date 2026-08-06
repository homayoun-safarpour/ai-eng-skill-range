import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "check.py"
        spec = importlib.util.spec_from_file_location("chk", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ev = [{"tool": "read"}, {"tool": "shell"}]
        if not mod.has_forbidden(ev, ["shell"]):
            return 2
        if mod.has_forbidden(ev, ["delete"]):
            return 2
        return 0
    except Exception:
        return 2
