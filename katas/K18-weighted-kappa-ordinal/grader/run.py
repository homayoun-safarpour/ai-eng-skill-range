import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "kappa.py"
        spec = importlib.util.spec_from_file_location("wk", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # The grader holds its own expected values. Each pair has a linear-weighted
        # value that differs from the unweighted and the quadratic-weighted value.
        cases = [
            ([0, 1, 2, 2], [0, 1, 2, 2], 1.0),
            ([0, 1, 2, 2], [0, 2, 1, 2], 3 / 7),  # unweighted 0.2, quadratic 7/11
            ([0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 1, 3, 2, 1, 3, 2], 9 / 19),  # unweighted 1/3, quadratic 11/18
        ]
        for y1, y2, expected in cases:
            got = float(mod.weighted_kappa(list(y1), list(y2)))
            if not abs(got - expected) <= 1e-6:
                print(f"FAIL: weighted_kappa({y1}, {y2}) = {got}; expected {expected:.6f}")
                return 2
        return 0
    except Exception:
        return 2
