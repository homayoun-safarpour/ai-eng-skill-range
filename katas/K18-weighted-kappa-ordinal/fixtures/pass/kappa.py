def weighted_kappa(y1, y2, weights="linear"):
    assert len(y1) == len(y2) and y1
    labels = sorted(set(y1) | set(y2))
    idx = {l: i for i, l in enumerate(labels)}
    k = len(labels)
    n = len(y1)
    o = [[0] * k for _ in range(k)]
    for a, b in zip(y1, y2):
        o[idx[a]][idx[b]] += 1
    w = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            w[i][j] = abs(i - j) / (k - 1) if k > 1 else 0.0
    row = [sum(o[i][j] for j in range(k)) for i in range(k)]
    col = [sum(o[i][j] for i in range(k)) for j in range(k)]
    e = [[row[i] * col[j] / n for j in range(k)] for i in range(k)]
    num = sum(w[i][j] * o[i][j] for i in range(k) for j in range(k))
    den = sum(w[i][j] * e[i][j] for i in range(k) for j in range(k))
    if den == 0:
        return 1.0
    return 1.0 - num / den
