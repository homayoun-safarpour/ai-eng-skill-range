# K22 : Offline lexical judge

Time box: 2h.

Implement `judge.py` with `pass_fail(answer, must_include: list[str]) -> str` returning pass if all needles appear in answer casefold else fail.

## Common fail

Calling an external LLM API fails. Keep the judge lexical/offline.
