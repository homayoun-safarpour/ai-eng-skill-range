import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "decide.py"
        spec = importlib.util.spec_from_file_location("dec", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if mod.decide({"tests": False, "lint": True}, "M1") != "repair:tests":
            return 2
        if mod.decide({"tests": True, "lint": True}, "M1") != "advance:M1":
            return 2
        return 0
    except Exception:
        return 2
