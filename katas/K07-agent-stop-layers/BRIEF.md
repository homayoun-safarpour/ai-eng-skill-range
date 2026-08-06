# K07 : Stop layers on disk

Time box: 1h.

Provide `stop_layers.json` with keys goal, max_turns, budget, no_progress (all non-empty strings).

## Common fail

Using different key names (`maxTurns`, `token_budget`) or leaving a value as `""`
fails the grader. All four keys must be present and non-empty strings.
