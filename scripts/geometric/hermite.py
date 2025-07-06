import numpy as np
from matplotlib import pyplot as plt



def hermite(p, n):
    """
    Returns n sample points on a d-dimensional hermite curve as a (n x d) matrix
    :param p: The four d-dimensional control points (4 x d)
    :param n: The number of samples
    """
    
    # coefficient matrix (4 x 4)
    m = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ])
    
    # computer graphics representation, where tangent vectors point inward.
    i = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])
    
    # powers of t for all n samples (n x 4)
    t = np.array([[t**3, t**2, t, 1] for t in np.linspace(0, 1, n)])
    
    # sample points of the hermite curve (n x d) = (n x 4) @ (4 x 4) @ (4 x d)
    return t @ m @ i @ p


if __name__ == '__main__':
    
    n = 50
    
    p0 = np.array([
        [0.2, 0.1],
        [0.5, 0.7],
        [2.0, 4.1],
        [-1.0, 0.4]
    ])
    
    p1 = np.array([
        p0[1],
        [0.9, 0.5],
        -2 * p0[3],
        [-0.1, -2]
    ])
    
    h0 = hermite(p0, n)
    h1 = hermite(p1, n)
    
    # plot tangent vectors
    plt.quiver(*p0[:2].T, *p0[2:].T)
    plt.quiver(*p1[:2].T, *p1[2:].T)
    
    # spread both dimensions *(n x d=2)^T = *(d=2 x n) = (1 x n), (1 x n)
    plt.plot(*h0.T)
    plt.plot(*h1.T)
    
    plt.gca().set_aspect('equal')
    plt.grid(True, which='both')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    plt.show()    
