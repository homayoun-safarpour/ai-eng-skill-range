# K13 — Drift attribution toy

Time box: 2h.

Implement `attr.py` with `verdict(base_kappa, cur_kappa, live_moved: bool, drop=0.1) -> str`:
JUDGE_DRIFT if kappa dropped by >= drop; else SYSTEM_CHANGE if live_moved; else STABLE.

## Common fail

Checking live_moved before kappa drop fails. JUDGE_DRIFT wins when kappa falls by >= drop even if live also moved.

## Example fill

```python
verdict(0.80, 0.50, live_moved=True, drop=0.1)  # JUDGE_DRIFT (kappa drop wins)
verdict(0.80, 0.78, live_moved=True, drop=0.1)  # SYSTEM_CHANGE
verdict(0.80, 0.79, live_moved=False, drop=0.1) # STABLE
```
