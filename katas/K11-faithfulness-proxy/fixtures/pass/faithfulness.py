def score(answer, context):
    toks = [t for t in answer.casefold().split() if t]
    if not toks:
        return 1.0
    ctx = set(context.casefold().split())
    return sum(1 for t in toks if t in ctx) / len(toks)
