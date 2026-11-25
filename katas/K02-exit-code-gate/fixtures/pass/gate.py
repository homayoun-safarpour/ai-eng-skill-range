import json
import sys
from pathlib import Path

path = Path(__file__).with_name("status.json")
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except (OSError, ValueError) as exc:
    print(f"FAIL: cannot read status.json: {exc}")
    sys.exit(2)
ok = data.get("ok") if isinstance(data, dict) else None
if not isinstance(ok, bool):
    print("FAIL: ok must be true or false")
    sys.exit(2)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 2)
