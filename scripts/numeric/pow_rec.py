def pow_rec(b, n):
    if n == 0: return 1
    if n % 2 == 0: return pow_rec(b, n / 2)**2
    return pow_rec(b, n-1) * b
