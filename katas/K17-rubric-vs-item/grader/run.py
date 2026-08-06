import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "cause.py"
        spec = importlib.util.spec_from_file_location("cause", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        c = mod.cause
        if c(True, True) != "both":
            return 2
        if c(True, False) != "item":
            return 2
        if c(False, True) != "rubric":
            return 2
        if c(False, False) != "neither":
            return 2
        return 0
    except Exception:
        return 2
