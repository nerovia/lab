import numpy as np
from matplotlib import pyplot as plt

def quadratic_bspline(P, T):
    # coefficient matrix
    M = 1/2 * np.array([
        [1, -2, 1],
        [-2, 2, 0],
        [1, 1, 0]
    ])
    
    # powers of t for all n samples (n x 3)
    T = np.array([[t**2, t, 1] for t in T])
    
    return T @ M @ P

def cubic_bspline(P, T):
    # coefficient matrix
    M = 1/6 * np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 0, 3, 0],
        [1, 4, 1, 0]
    ])
    
    # powers of t for all n samples (n x 3)
    T = np.array([[t**3, t**2, t, 1] for t in T])
    
    return T @ M @ P


if __name__ == '__main__':
    
    P = np.array([
        [1, 0.2],
        [1, 0.2],
        [0, 1],
        [-1.2, 0.5],
        [0, -1]
    ])
    
    # plot closed quadratic bezier spline
    T = np.linspace(0, 1)
    m = len(P)
    for i in range(1, m+1):
        b2 = quadratic_bspline(np.array([P[j%m] for j in range(i-1, i+2)]), T)
        plt.plot(*b2.T, color='blue')
    
    # plot closed cubic bezier spline
    for i in range(1, m+2):
        b3 = cubic_bspline(np.array([P[j%m] for j in range(i-1, i+3)]), T)
        plt.plot(*b3.T, color='red')
        
    plt.scatter(*P.T)
    
    plt.gca().set_aspect('equal')
    plt.grid(True, which='both')
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    
    plt.show()    
