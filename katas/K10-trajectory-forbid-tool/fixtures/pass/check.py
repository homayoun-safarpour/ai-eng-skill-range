def has_forbidden(events, forbidden):
    bad = set(forbidden)
    return any(e.get("tool") in bad for e in events)
