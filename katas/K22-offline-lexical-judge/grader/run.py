import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "judge.py"
        spec = importlib.util.spec_from_file_location("j", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if mod.pass_fail("Hello World", ["hello"]) != "pass":
            return 2
        if mod.pass_fail("Hello", ["hello", "world"]) != "fail":
            return 2
        return 0
    except Exception:
        return 2
