import numpy as np
from matplotlib import pyplot as plt


def dragonize(p: np.ndarray):
    '''
    Generates the next iteration of the dragon curve on a list of points p.
    '''
    t = list(p[:1])
    for i in range(1, len(p)):
        v = p[i] - p[i-1]

        # everyday use of the perp-vector
        u0, u1 = v[1] + v[0], v[1] - v[0]  # (v0, v1) = (u0, u1) + (-u1, u0)
        u = np.array([-u1, u0] if i%2 else [u0, u1])

        t.append(p[i-1] + u/2)  # normalize u, since we skipped that before
        t.append(p[i])

    return np.array(t)


def chaikin(p: list):
    '''
    Applies Chaikin's refinement method on a list of points p.
    Approximates a quadratic b-spline if iterated.
    '''
    t = []
    for i in range(1, len(p)):
        t.append(.75 * p[i-1] + .25 * p[i])
        t.append(.25 * p[i-1] + .75 * p[i])

    return np.array(t)


def dragon_spline(d, k):
    '''
    Approximates a b-spline in k iterations to fit a dragon curve of d iterations.
    '''
    p = np.array([[-1, 1], [1, -1]])# generator points
    
    for _ in range(d):  # generate dragon curve
        p = dragonize(p)
    for _ in range(k):  # approximate spline
        p = chaikin(p)

    return p


if __name__ == '__main__':
    d = 10  # iterations of the dragon curve
    k = 4   # iterations of Chaikin's method
    p = dragon_spline(d, k)

    plt.gca().set_aspect('equal')
    
    plt.plot(*p.T)
    plt.savefig('img/dragon.png')
    plt.show()    
