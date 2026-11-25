import importlib.util
from pathlib import Path

def _load(submission: Path):
    path = submission / "kappa.py"
    spec = importlib.util.spec_from_file_location("kappa_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.cohen_kappa

def grade(submission: Path) -> int:
    # The grader holds its own expected values.
    cases = [
        (["a", "a", "b", "b"], ["a", "a", "b", "b"], 1.0),  # perfect agreement
        (["a", "a", "b", "b"], ["b", "b", "a", "a"], -1.0),  # total disagreement
        (["a", "a", "b", "b"], ["a", "b", "b", "b"], 0.5),  # partial; percent agreement is 0.75
        (["a", "a", "a", "a"], ["a", "a", "a", "a"], 1.0),  # both raters constant: perfect agreement
    ]
    try:
        fn = _load(submission)
        for y1, y2, expected in cases:
            got = float(fn(list(y1), list(y2)))
            if not abs(got - expected) <= 1e-6:
                print(f"FAIL: cohen_kappa({y1}, {y2}) = {got}; expected {expected}")
                return 2
        return 0
    except Exception:
        return 2
