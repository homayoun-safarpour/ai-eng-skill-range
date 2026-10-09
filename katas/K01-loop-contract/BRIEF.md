# K01 : Loop Contract

Time box: 1–2h.

Fill `LOOP_CONTRACT.md` with the five required decision headings used before
automating an agent loop. The default grader checks heading presence only.
Use `skillrange grade K01 --submission <directory> --strict` to require
non-comment content in each section. Empty sections and HTML-comment-only
sections fail strict grading with exit 2; the existing default is unchanged.

## Example fill : CI triage loop

Use this as a worked shape for a **CI triage** loop (synthetic; no secrets, no
private tokens). Copy the structure into your submission; change the details to
match your repo.

### 1. Done
`gh run list --limit 1` shows the latest workflow `conclusion=success`, and
`pytest -q` exits 0 on the failing job's package locally.

### 2. Verifier
CI logs + local `pytest -q` (not the same agent that proposed the fix).

### 3. Stop layers
Goal = green CI on `main` for the named workflow; max 8 ticks; stop after
2 ticks with no new failing test name.

### 4. State file
`LOOP_STATE.md` with the failing job URL, last error signature, and next command.

### 5. Irreversible
`gh workflow run` against production deploy workflows and any `git push --force`
need an explicit human yes in the state file.

## Common fail

Skipping a numbered heading fails either mode. Filling a section with HTML
comments only fails strict mode. All five decision headings need real content
to pass strict grading.
