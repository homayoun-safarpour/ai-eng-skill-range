import importlib.util
from pathlib import Path

def _load(submission: Path):
    path = submission / "kappa.py"
    spec = importlib.util.spec_from_file_location("kappa_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.cohen_kappa

def grade(submission: Path) -> int:
    try:
        fn = _load(submission)
        if abs(fn(["a", "a", "b", "b"], ["a", "a", "b", "b"]) - 1.0) > 1e-6:
            return 2
        # total disagreement on balanced binary -> kappa  -1 or low
        k = fn(["a", "a", "b", "b"], ["b", "b", "a", "a"])
        if k > -0.9:
            return 2
        return 0
    except Exception:
        return 2
