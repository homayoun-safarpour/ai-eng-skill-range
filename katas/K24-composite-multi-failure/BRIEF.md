# K24 — Composite multi-failure

Time box: 2h.

Implement `detect.py` with `failures(events, forbidden, required) -> list[str]` returning any of `forbidden_tool`, `missing_tool` that apply.

## Common fail

Reporting only the first failure mode fails. Surface the composite / multi-failure contract the rubric names.
