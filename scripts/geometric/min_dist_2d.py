import math
import random

def min_dist_2d(lst):
    
    # base case
    n = len(lst)
    if n <= 3:
        min_d = float('inf')
        for i in range(0, n):
            for j in range(i+1, n):
                min_d = min(min_d, dist_2d(lst[i], lst[j]))
        return min_d
    
    # decomposition & recursive step
    lst.sort(key=lambda it: it[0])             # sort points by x
    m = int(n / 2)
    min_b = min_dist_2d(lst[m:])
    min_a = min_dist_2d(lst[:m])

    # reconstruction
    min_d = min(min_b, min_a)
    win = [it for it in lst if min_d > abs(it[0] - lst[m][0])]
    win.sort(key=lambda it: it[1])
    w = len(win)
    for i in range(0, w): # check the window for points that have been overlooked
        for j in range(i+1, w):
            if min_d > abs(lst[i][1] - lst[j][1]):
                min_d = min(min_d, dist_2d(win[i], win[j]))
            else: break   # skip if the vertical distance exceeds threshold

    return min_d


def dist_2d(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.sqrt(dx * dx + dy * dy)

def brute_force(lst):
    n = len(lst)
    min_d = float('inf')
    for i in range(0, n):
        for j in range(i+1, n):
            min_d = min(min_d, dist_2d(lst[i], lst[j]))
    return min_d

if __name__ == "__main__":
    # print("min dist is:", min_dist_1d([8, 11, 15, 4]))
    for j in range(0, 10):
        arr = []
        for i in range(0, 1000):
            arr.append((random.uniform(-1, 1), random.uniform(.1, 1)))
        b = brute_force(arr)
        a = min_dist_2d(arr)
        if a != b:
            print("oh oh")
        print("min dist is:", a)
        print("brute force:", b)

