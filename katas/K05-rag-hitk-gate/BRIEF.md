# K05 — hit@k / MRR gate

Time box: 2–3h.

Implement `metrics.py` with `hit_at_k(ranking, relevant, k)` and `mrr(ranking, relevant)`.

## Common fail

Using 1-based rank math incorrectly (off-by-one on `k`), or returning MRR over the
full list when no relevant id appears, fails the grader. Empty `relevant` must follow
the rubric edge case, not crash.
