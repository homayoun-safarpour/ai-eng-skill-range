# K21 — Absolute paths ACI

Time box: 1h.

Implement `ok_path(p: str) -> bool` True only for absolute paths (POSIX `/` or Windows drive `C:\\`).

## Common fail

Relative paths that break when cwd changes fail ACI checks. Prefer absolute paths in the contract.
