# K17 — Rubric vs item ambiguity

Time box: 2h.

Implement `cause.py` with `cause(item_ambiguous: bool, rubric_vague: bool) -> str` returning `item` | `rubric` | `both` | `neither`.

## Common fail

Returning only item/rubric without both/neither fails the truth table. Encode all four combinations.
