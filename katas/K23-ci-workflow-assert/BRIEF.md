# K23 : CI workflow assert

Time box: 1h.

Provide `.github/workflows/ci.yml` that contains `jobs:` and `pytest` somewhere in the file.

## Common fail

A workflow that never runs pytest (or the named gate) fails. Assert the job steps exist.
