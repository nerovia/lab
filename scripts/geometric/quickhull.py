import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt
from numpy.typing import ArrayLike

def perp(u, v):
    return u[0] * v[1] - u[1] * v[0]

def left_of(u, v):
    """Returns true if c is to the left of ab"""
    return perp(u, v)

def quickhull(S: ArrayLike):
    l = [min(S, key=lambda p: p[0])]
    r = [max(S, key=lambda p: p[0])]
    
    
    
    lr = r-l
    hull = [l, r]
    left = [v for v in S if perp(lr, v-l) < 0]
    right = [v for v in S if perp(lr, v-l) >= 0]
    
    
    

def findhull(lst: list, hull: list, i, j):
    if len(lst) == 0:
        return
    a = hull[i]
    b = hull[j]
    
    ab = b - a

    c = max(lst, key=lambda v: perp(ab, v-a))
    hull = hull[:i] + [c] + hull[i:]
    
    left = [v for v in S if perp(lr, v-l) < 0]
    right = [v for v in S if perp(lr, v-l) >= 0]
    
                


if __name__ == '__main__':
    S = np.array([[4, 5], [1, 2], [5, -4], [-6,-3], [-5, -1], [-4, 5], [0, 2]])
    H = gift_warp(S)
    
    plt.axis('equal')
    plt.fill(*S.T)
    plt.plot(*np.vstack([*S, S[0]]).T, '.r', linestyle='solid')
    plt.plot(*np.vstack([*H, H[0]]).T, '.g', linestyle='dotted')
    plt.show()
   
    