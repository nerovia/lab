def float_cmp(a, b, epsilon):
    u = abs(u)
    v = abs(v)
    diff = abs(u - v)
    if a == b:
        return True
    elif a == 0 or b == 0 or u + v < FLOAT:
        return diff < epsilon * MIN_NORMAL_FLOAT
    else
        return diff / min(u + v, MAX_VALUE)