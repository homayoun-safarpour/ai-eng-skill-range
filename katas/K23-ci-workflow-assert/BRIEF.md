# K23 : CI workflow assert

Time box: 1h.

Provide `.github/workflows/ci.yml` with a `jobs:` key and a `run:` step under `steps:` that calls `pytest`. A mention of pytest in a comment or a name does not count.

## Common fail

A workflow that never runs pytest (or the named gate) fails. Assert the job steps exist.
