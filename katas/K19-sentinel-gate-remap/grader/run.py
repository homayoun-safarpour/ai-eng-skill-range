import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "remap.py"
        spec = importlib.util.spec_from_file_location("rm", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if mod.remap(0) != 0 or mod.remap(3) != 0:
            return 2
        if mod.remap(2) != 2:
            return 2
        if mod.remap(1) != 1:
            return 2
        return 0
    except Exception:
        return 2
