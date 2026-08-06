import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "diagnose.py"
        spec = importlib.util.spec_from_file_location("diag", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        d = mod.diagnose
        if d(["a"], ["b"], False) != "retrieval":
            return 2
        if d(["a", "b"], ["a"], True) != "generation":
            return 2
        if d(["a", "b"], ["a"], False) != "ok":
            return 2
        return 0
    except Exception:
        return 2
