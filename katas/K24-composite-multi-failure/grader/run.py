import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "detect.py"
        spec = importlib.util.spec_from_file_location("det", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ev = [{"tool": "shell"}, {"tool": "read"}]
        got = mod.failures(ev, ["shell"], ["write"])
        if "forbidden_tool" not in got or "missing_tool" not in got:
            return 2
        if mod.failures([{"tool": "read"}], ["shell"], ["read"]):
            return 2
        return 0
    except Exception:
        return 2
