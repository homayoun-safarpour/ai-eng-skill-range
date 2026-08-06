import hashlib
import json
from pathlib import Path

def grade(submission: Path) -> int:
    corpus = submission / "corpus.txt"
    base = submission / "baseline.json"
    if not corpus.is_file() or not base.is_file():
        return 2
    digest = hashlib.sha256(corpus.read_bytes()).hexdigest()
    data = json.loads(base.read_text(encoding="utf-8"))
    return 0 if data.get("corpus_sha256") == digest else 2
