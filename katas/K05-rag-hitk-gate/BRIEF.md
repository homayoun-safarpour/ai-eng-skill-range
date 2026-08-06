# K05 — hit@k / MRR gate

Time box: 2–3h.

Implement `metrics.py` with `hit_at_k(ranking, relevant, k)` and `mrr(ranking, relevant)`.

## Example fill

```python
ranking = ["d3", "d1", "d9"]
relevant = {"d1", "d7"}
hit_at_k(ranking, relevant, k=2)  # True — d1 is in the top-2
mrr(ranking, relevant)            # 0.5 — first relevant hit at rank 2
```

## Common fail

Using 1-based rank math incorrectly (off-by-one on `k`), or returning MRR over the
full list when no relevant id appears, fails the grader. Empty `relevant` must follow
the rubric edge case, not crash.
