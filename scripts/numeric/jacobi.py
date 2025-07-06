import numpy as np
from numpy.linalg import norm, vector_norm
from numpy.typing import ArrayLike

def jacobi(a: ArrayLike, b: ArrayLike, epsilon: float, max_iter = 1000):
    (n, m) = np.shape(a)
    if n != m: raise ValueError('must be square matrix')
    
    x0 = np.array([0.0] * n)
    x1 = x0.copy()
    
    for k in range(max_iter):
        
        for i in range(n):
            sigma = sum(a[i,j] * x0[j] for j in range(n) if j != i)
            x1[i] = (b[i] - sigma) / a[i,i]     
        
        if norm(x1 - x0) < epsilon:
            print(f'convergence reached afer {k} iterations')
            return x1
        
        x0 = x1.copy()
        
    print('iterations exceeded')
    return x0


if __name__ == '__main__':
    a = np.array([[2.0, 1.0], [5.0, 7.0]])
    b = np.array([11.0, 13.0])
    x = jacobi(a, b, 0.0001)
    print(x)