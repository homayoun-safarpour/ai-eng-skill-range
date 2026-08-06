def verdict(base_kappa, cur_kappa, live_moved, drop=0.1):
    if base_kappa - cur_kappa >= drop:
        return "JUDGE_DRIFT"
    if live_moved:
        return "SYSTEM_CHANGE"
    return "STABLE"
