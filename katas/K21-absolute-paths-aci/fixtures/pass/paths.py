from pathlib import Path

def ok_path(p):
    return Path(p).is_absolute()
