# K08 : Tool schema validate

Time box: 2h.

Implement `validate.py` with `validate_tool(call: dict, schema: dict) -> bool`.
Schema: `{"name": str, "required": [str]}`. Call must match name and include required args keys.

## Common fail

Accepting a call with the right name but missing a required arg key, or ignoring a
name mismatch when args look fine, fails the grader. Extra args are usually OK;
missing required keys are not.
