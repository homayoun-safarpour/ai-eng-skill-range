import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "paths.py"
        spec = importlib.util.spec_from_file_location("paths", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if mod.ok_path("relative/file.txt"):
            return 2
        if not mod.ok_path("/tmp/x") and not mod.ok_path("C:\\tmp\\x"):
            # at least one absolute style must work on this OS
            if not mod.ok_path(str(Path.cwd() / "x")):
                # Path.cwd()/x is absolute
                return 2
        if not mod.ok_path(str(Path.cwd() / "abs.txt")):
            return 2
        return 0
    except Exception:
        return 2
