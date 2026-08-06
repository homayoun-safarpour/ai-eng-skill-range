# K13 — Drift attribution toy

Time box: 2h.

Implement `attr.py` with `verdict(base_kappa, cur_kappa, live_moved: bool, drop=0.1) -> str`:
JUDGE_DRIFT if kappa dropped by >= drop; else SYSTEM_CHANGE if live_moved; else STABLE.

## Common fail

Checking live_moved before kappa drop fails. JUDGE_DRIFT wins when kappa falls by >= drop even if live also moved.
