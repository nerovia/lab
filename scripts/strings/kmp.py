import sys


def brute_force_match(s, p):
    n = len(s)
    m = len(p)
    for i in range(0, n-m):
        j = 0
        while j < m and s[i + j] == p[j]: j += 1
        if j == m: return i
    return -1


def kmp_fail(p):
    # Returns the prefix table of the given string

    m = len(p)
    f = [0] * m
    i = 0
    j = 1
    while j < m:
        if p[i] == p[j]:
            i += 1
            f[j] = i
            j += 1
        elif 0 < i:
            i = f[i-1]
        else:
            f[j] = 0
            j += 1
    return f


def kmp_match(s, p):
    # Returns the index of the first appearance 
    # of the pattern string in the candidate string.

    f = kmp_fail(p)
    n = len(s)
    m = len(p)
    i = 0
    j = 0

    while i < n:
        if s[i] == p[j]:
            if j == m - 1: 
                return i - j
            i += 1
            j += 1
        elif 0 < j:
            j = f[j-1]
        else:
            i += 1
    return -1
    

if __name__ == "__main__":
    s = sys.argv[1]
    p = sys.argv[2]
    i = kmp_match(s, p)
    print(i)