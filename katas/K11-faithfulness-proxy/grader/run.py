import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "faithfulness.py"
        spec = importlib.util.spec_from_file_location("faith", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if abs(mod.score("", "anything") - 1.0) > 1e-9:
            return 2
        if abs(mod.score("red cat", "the red ball") - 0.5) > 1e-9:
            return 2
        return 0
    except Exception:
        return 2
