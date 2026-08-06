# K10 : Forbidden tool in trajectory

Time box: 1–2h.

Implement `check.py` with `has_forbidden(events, forbidden) -> bool`.
Events are list of `{tool: str}`.

## Common fail

Returning True only when every event is forbidden fails. Any single forbidden tool in the list must be detected.
