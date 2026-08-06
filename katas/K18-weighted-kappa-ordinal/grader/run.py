import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "kappa.py"
        spec = importlib.util.spec_from_file_location("wk", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        y = [0, 1, 2, 2]
        if abs(mod.weighted_kappa(y, y) - 1.0) > 1e-6:
            return 2
        return 0
    except Exception:
        return 2
