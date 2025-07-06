def binom(n, k):
    acc = 1
    for i in range(1, k):
        acc *= (n + 1 - i) / i
    return acc

if __name__ == "__main__":
    print(binom(3, 2))
