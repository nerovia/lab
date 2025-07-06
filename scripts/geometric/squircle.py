import numpy as np  
from hermite import hermite
from matplotlib import pyplot as plt

if __name__ == '__main__':
    
    n = 50
    l = 2
    
    P = np.array([
        [[1, 0], [0, 1], [0, l], [l, 0]],
        [[0, 1], [-1, 0], [-l, 0], [0, l]],
        [[-1, 0], [0, -1], [0, -l], [-l, 0]],
        [[0, -1], [1, 0], [l, 0], [0, -l]]
    ])
    
    for p in P:
        h = hermite(p, n)
        plt.quiver(*p[:2].T, *p[2:].T)
        plt.plot(*h.T)
    
    plt.gca().set_aspect('equal')
    plt.grid(True, which='both')
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    
    plt.show()    
