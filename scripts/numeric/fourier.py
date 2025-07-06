import numpy as np
from matplotlib import pyplot as plt
from bspline import quadratic_bspline

def dft(x):
    """
    Transforms N samples from the time to frequency domain
    Returns the coefficients of a fourier series
    """
    N = len(x)
    X = np.array([
        sum([x[n] * np.exp(-2*np.pi * 1.j * k/N * n) for n in range(N)])
        for k in range(N)
    ])
    return X
    
def idft(X):
    """
    Transforms N samples from frequency to time domain
    """
    N = len(X)
    x = np.array([
        1/N * sum([X[n] * np.exp(2*np.pi * 1.j * k/N * n) for n in range(N)])
        for k in range(N)
    ])
    return x
    

def fourier(t, c):
    """
    Evaluates a fourier series at paramter t.
    :param t: the parameter at which to evaluate (with a periodicity of 1)
    :param c: the N coefficients of the fourier series  
    """
    N = len(c)
    return 1/N * sum([
        c[n] * np.exp(2*np.pi * 1.j * n * t)
        for n in range(0, N)
    ])
    

    
if __name__ == '__main__':
    
    N = 4
    P = np.array([
        [1, 0.2],
        [0, 1],
        [-1.2, 0.5]
    ])
    
    T = np.linspace(0, 1, N)

    b = quadratic_bspline(P, T)
    
    x = b[:,0] + 1.j * b[:,1]
    
    c = dft(x)
    
    # print(x)
    # print(c)
    # print(idft(c))
    
    print(b)
   
    s = np.array([
        [np.real(x:=fourier(t, c)), np.imag(x)]
        for t in np.linspace(0, 1, 100)
    ])
    
    
    plt.plot(*b.T)
    plt.plot(*s.T)
    
    plt.gca().set_aspect('equal')
    plt.grid(True, which='both')
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    
    plt.show()    