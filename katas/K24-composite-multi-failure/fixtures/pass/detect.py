def failures(events, forbidden, required):
    tools = [e.get("tool") for e in events]
    out = []
    if any(t in set(forbidden) for t in tools):
        out.append("forbidden_tool")
    if any(r not in tools for r in required):
        out.append("missing_tool")
    return out
