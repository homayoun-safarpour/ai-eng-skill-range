# K02 — Exit-code gate

Time box: 1–2h.

Implement `gate.py` that reads `status.json` with key `ok` (bool).
Print PASS/FAIL and exit 0 when ok is true, else exit 2.

## Common fail

Exiting `1` on failure (or raising) fails the grader. The contract is **exit 2** for
FAIL so CI can treat it as a quality gate, not a crash. Missing `status.json` or a
non-bool `ok` should also FAIL with exit 2, not traceback exit 1.
