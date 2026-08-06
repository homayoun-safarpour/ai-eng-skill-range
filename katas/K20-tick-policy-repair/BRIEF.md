# K20 : Tick policy repair-before-advance

Time box: 2h.

Implement `decide(gates: dict[str,bool], head: str) -> str` returning `repair:<gate>` if any gate False, else `advance:<head>`.

## Common fail

Letting a red gate advance backlog work fails. Repair must beat progress.
