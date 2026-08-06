def hit_at_k(ranking, relevant, k):
    rel = set(relevant)
    return 1.0 if any(x in rel for x in ranking[:k]) else 0.0

def mrr(ranking, relevant):
    rel = set(relevant)
    for i, x in enumerate(ranking, 1):
        if x in rel:
            return 1.0 / i
    return 0.0
