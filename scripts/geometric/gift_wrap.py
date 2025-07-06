import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import ArrayLike

def left_of(a, b, c):
    """Returns true if c is to the left of ab"""
    u = b - a
    v = c - a
    return u[0]*v[1] - u[1]*v[0] < 0

def gift_warp(V: ArrayLike):
    H = [min(V, key=lambda p: p[0])]
    
    while True:
        p = V[0]
        
        for q in V:
            if (p == H[-1]).all() or left_of(p, H[-1], q):
                p = q
                
        if (p == H[0]).all():
            return np.array(H)
        
        H.append(p)
        
                


if __name__ == '__main__':
    S = np.array([[4, 5], [1, 2], [5, -4], [-6,-3], [-5, -1], [-4, 5], [0, 2]])
    H = gift_warp(S)
    
    plt.axis('equal')
    plt.fill(*S.T)
    plt.plot(*np.vstack([*S, S[0]]).T, '.r', linestyle='solid')
    plt.plot(*np.vstack([*H, H[0]]).T, '.g', linestyle='dotted')
    plt.show()
   
    