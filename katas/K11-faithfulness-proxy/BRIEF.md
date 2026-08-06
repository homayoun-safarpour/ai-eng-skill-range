# K11 — Offline faithfulness proxy

Time box: 2h.

Implement `faithfulness.py` with `score(answer: str, context: str) -> float` in [0,1]: fraction of answer tokens (whitespace) that appear in context (casefold).

## Common fail

Case-sensitive token compare, or scoring characters instead of whitespace tokens, fails the grader. Use casefold and [0,1].
