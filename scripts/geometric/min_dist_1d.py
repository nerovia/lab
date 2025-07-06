import math
import random

def min_dist_1d(lst):
    lst.sort()
    return min_dist_1d_rec(lst)


def min_dist_1d_rec(lst):

    # base case
    n = len(lst)
    if n == 2:
        return abs(lst[0] - lst[1])
    if n == 3:
        return min(abs(lst[0] - lst[1]), abs(lst[1] - lst[2]))
    
    # decomposition & recursive step
    m = int(n / 2)
    min_l = min_dist_1d_rec(lst[:m])
    min_r = min_dist_1d_rec(lst[m:])

    # reconstruction
    d = min(min_l, min_r, abs(lst[m - 1] - lst[m]))
    return d


def min_dist_2d(lst):
    
    # base case
    n = len(lst)
    if n <= 3:
        min_d = float('inf')
        for i in range(0, n):
            for j in range(i+1, n):
                min_d = min(min_d, dist_2d(lst[i], lst[j]))
        return min_d
    
    # decomposition
    lst.sort(key=lambda it: it[0])             # sort points by x
    mid = lst[int(len(lst) / 2)]               # find the middle x
    lst.sort(key=lambda it: it[1])             # sort points by y
    b = [it for it in lst if it[0] < mid[0]]   # split points below x
    a = [it for it in lst if it[0] >= mid[0]]  # split points above x

    # recursive step
    min_b = min_dist_2d(b)
    min_a = min_dist_2d(a)

    # reconstruction
    min_d = min(min_b, min_a)
    win = [it for it in lst if abs(it[0] - mid[0])]
    w = len(win)
    for i in range(0, w): # check the window for points that have been overlooked
        for j in range(i+1, w):
            min_d = min(min_d, dist_2d(win[i], win[j]))

    return min_d


def dist_2d(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.sqrt(dx * dx + dy * dy)

if __name__ == "__main__":
    # print("min dist is:", min_dist_1d([8, 11, 15, 4]))
    math.
    print("min dist is:", min_dist_2d([(1, 1), (1, -2), (-2, 1), (-1, -1)]))
