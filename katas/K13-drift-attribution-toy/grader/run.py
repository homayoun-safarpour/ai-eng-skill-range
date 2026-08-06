import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "attr.py"
        spec = importlib.util.spec_from_file_location("attr", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        v = mod.verdict
        if v(0.9, 0.7, True) != "JUDGE_DRIFT":
            return 2
        if v(0.9, 0.89, True) != "SYSTEM_CHANGE":
            return 2
        if v(0.9, 0.89, False) != "STABLE":
            return 2
        return 0
    except Exception:
        return 2
