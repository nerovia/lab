import numpy as np
from numpy.typing import ArrayLike

def lu_decompose(a: ArrayLike):
    (n, m) = np.shape(a)
    if n != m: raise ValueError('must be square matrix')
    
    u = np.array([[0] * n] * n)
    l = np.array([[0] * n] * n)
    
    for i in range(n):
        # set the diagonal entry for L
        l[i,i] = 1
        
        # compute the i-th row of U
        for j in range(i, n):
            term = sum(l[i, k] * u[k, j] for k in range(i))
            # solve for u_ij
            u[i,j] = a[i,j] - term
            
        # compute the i-th column of L
        for j in range(i+1, n):
            term = sum(l[j, k] * u[k, i] for k in range(i))
            # solve for l_ij
            l[j,i] = 1/u[i,i] * (a[j,i] - term)
    
    return (l, u)
    
    
    
if __name__ == '__main__':
    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    (l, u) = lu_decompose(a)
    print('a =', a, sep='\n')
    print('l =', l, sep='\n')
    print('u =', u, sep='\n')
    print('l*u =', l @ u, sep='\n')
    