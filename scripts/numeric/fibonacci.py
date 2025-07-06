
def fib_rec(n):
    if n <= 0: return n
    return fib_rec(n-1) + fib_rec(n-2)


def fib_mat(n):
	return fib_mat_mul(0, 1, 1, 1, n)


def fib_mat_mul(a11, a12, a21, a22, n):
	if n <= 0: return a11
	return fib_mat_mul(a21, a22, a11+a21, a12+a22, n-1)
