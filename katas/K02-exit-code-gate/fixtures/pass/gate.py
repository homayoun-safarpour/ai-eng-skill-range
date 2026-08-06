import json, sys
from pathlib import Path
data = json.loads(Path(__file__).with_name('status.json').read_text(encoding='utf-8'))
ok = bool(data.get('ok'))
print('PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 2)
