import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "budget.py"
        spec = importlib.util.spec_from_file_location("bud", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not mod.within_budget(1.0, 1.0):
            return 2
        if mod.within_budget(1.01, 1.0):
            return 2
        return 0
    except Exception:
        return 2
