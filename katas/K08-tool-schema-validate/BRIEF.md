# K08 — Tool schema validate

Time box: 2h.

Implement `validate.py` with `validate_tool(call: dict, schema: dict) -> bool`.
Schema: `{"name": str, "required": [str]}`. Call must match name and include required args keys.
