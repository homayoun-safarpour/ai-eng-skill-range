# K04 — Cohen kappa for two raters

Time box: 2h.

Implement `kappa.py` exposing `cohen_kappa(y1, y2) -> float`.
Labels are parallel lists of strings. Grader checks known pairs.

## Common fail

Reporting percent agreement instead of Cohen's kappa, or returning `nan` when both
raters are constant, fails the grader. Use the same label universe for both lists
and handle the no-variance edge the way the rubric specifies.

