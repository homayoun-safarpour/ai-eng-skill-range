def validate_tool(call, schema):
    if call.get("name") != schema.get("name"):
        return False
    args = call.get("args") or {}
    for key in schema.get("required") or []:
        if key not in args:
            return False
    return True
