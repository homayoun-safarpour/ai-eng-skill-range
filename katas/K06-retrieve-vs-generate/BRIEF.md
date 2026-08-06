# K06 — Retrieve vs generate failure

Time box: 1–2h.

Write `diagnose.py` with `diagnose(retrieved_ids, relevant_ids, answer_has_hallucination: bool) -> str` returning `retrieval` | `generation` | `ok`.

## Common fail

Calling every wrong answer `generation` when the retrieved set missed the relevant
ids fails the grader. Order of checks matters: empty overlap with relevant ids is
`retrieval` before you blame the generator.
