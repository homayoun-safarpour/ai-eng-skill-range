import importlib.util
from pathlib import Path

def grade(submission: Path) -> int:
    try:
        path = submission / "validate.py"
        spec = importlib.util.spec_from_file_location("val", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        schema = {"name": "search", "required": ["q"]}
        if not mod.validate_tool({"name": "search", "args": {"q": "x"}}, schema):
            return 2
        if mod.validate_tool({"name": "other", "args": {"q": "x"}}, schema):
            return 2
        if mod.validate_tool({"name": "search", "args": {}}, schema):
            return 2
        return 0
    except Exception:
        return 2
