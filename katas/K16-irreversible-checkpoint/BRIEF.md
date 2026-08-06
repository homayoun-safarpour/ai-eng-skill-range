# K16 — Irreversible checkpoint

Time box: 1h.

Provide `checkpoints.json` listing irreversible actions each with `name` and `human_required: true`.
Need at least two entries.

## Common fail

human_required false, or fewer than two entries, fails. Every listed action needs human_required true.
