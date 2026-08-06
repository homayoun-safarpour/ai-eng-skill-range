import hashlib
import json
from pathlib import Path

def grade(submission: Path) -> int:
    data = submission / "data.bin"
    sig_path = submission / "signature.json"
    if not data.is_file() or not sig_path.is_file():
        return 2
    digest = hashlib.sha256(data.read_bytes()).hexdigest()
    sig = json.loads(sig_path.read_text(encoding="utf-8"))
    if sig.get("data_sha256") != digest:
        return 2
    if not str(sig.get("env") or "").strip():
        return 2
    return 0
