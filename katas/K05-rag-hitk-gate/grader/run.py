import importlib.util
from pathlib import Path

def _load(submission):
    path = submission / "metrics.py"
    spec = importlib.util.spec_from_file_location("metrics_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def grade(submission: Path) -> int:
    try:
        m = _load(submission)
        ranking = ["d1", "d2", "d3"]
        if m.hit_at_k(ranking, ["d2"], 2) != 1.0:
            return 2
        if m.hit_at_k(ranking, ["d3"], 2) != 0.0:
            return 2
        if abs(m.mrr(ranking, ["d2"]) - 0.5) > 1e-9:
            return 2
        return 0
    except Exception:
        return 2
