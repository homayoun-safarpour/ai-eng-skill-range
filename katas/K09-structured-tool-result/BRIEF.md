# K09 : Structured tool result

Time box: 1–2h.

Write `result.json` with keys tool, args_hash, status where status is ok|error.

## Common fail

Using `success`/`fail` instead of `ok`/`error`, or omitting `args_hash`, fails the
grader. Keys must be exactly `tool`, `args_hash`, and `status`.
