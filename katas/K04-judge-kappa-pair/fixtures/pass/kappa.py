def cohen_kappa(y1, y2):
    assert len(y1) == len(y2) and y1
    labels = sorted(set(y1) | set(y2))
    n = len(y1)
    # confusion
    idx = {l: i for i, l in enumerate(labels)}
    m = [[0] * len(labels) for _ in labels]
    for a, b in zip(y1, y2):
        m[idx[a]][idx[b]] += 1
    po = sum(m[i][i] for i in range(len(labels))) / n
    row = [sum(m[i][j] for j in range(len(labels))) for i in range(len(labels))]
    col = [sum(m[i][j] for i in range(len(labels))) for j in range(len(labels))]
    pe = sum((row[i] / n) * (col[i] / n) for i in range(len(labels)))
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)
