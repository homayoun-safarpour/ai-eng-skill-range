# K18 — Weighted kappa (ordinal)

Time box: 3h.

Implement `weighted_kappa(y1, y2, weights='linear')` for ordinal labels 0..n. Linear weights. Perfect agreement -> 1.0.

## Common fail

Unweighted Cohen kappa, or quadratic weights when linear is required, fails. Perfect agreement must be 1.0.
