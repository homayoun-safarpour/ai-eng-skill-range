def decide(gates, head):
    for name, ok in gates.items():
        if not ok:
            return f"repair:{name}"
    return f"advance:{head}"
