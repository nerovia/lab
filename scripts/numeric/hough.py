import numpy as np
from numpy.typing import ArrayLike
from PIL import Image, ImageColor

def hough_line_transform(I: ArrayLike, H: ArrayLike):
    (w, h) = np.shape(I)
    (m, n) = np.shape(H)
    
    r_max = 2.0 * np.sqrt(m**2 + h**2)
    
    for dy in range(h):
        for dx in range(w):
            x = dx - w/2
            y = dy - h/2
            
            if I[dx, dy] < 0.5: continue
            
            for dt in range(m):
                t = dt * np.pi / m
                r = x * np.cos(t) + y * np.sin(t)
                dr = int(n * r/r_max + n/2)
                H[dt, dr] += 1
    
    
def non_max_supressoin(M: ArrayLike, r: 2):
    (w, h) = np.shape(M)
    N = np.zeros((w, h))
    
    for y in range(h):
        for x in range(w):
            maximum = max([M[x+i, y+j] 
                for i in range(-r, r) if x+i in range(w)
                for j in range(-r, r) if y+j in range(h)])
            if M[x, y] == maximum:
                N[x, y] = maximum
            
    return N


def extract_lines(H: ArrayLike):
    (m, n) = np.shape(H)
    r_max = 2.0 * np.sqrt(m**2 + n**2)
    lst = []
    
    for dt in range(m):
        t = dt * np.pi / m
        for dr in range(n):
            r = (dr - n/2) * r_max/n
            if H[dr, dt] != 0:
                p0 = np.array([np.cos(t), np.sin(t)])
                p = np.array([-p0[1], p0[0]])
                lst.append((p0*r, p))
                

    return lst


im_in = Image.open('../res/textures/texture_0.png').convert('L')

I = np.asarray(im_in, dtype=float)
I = I / I.max();
H = np.zeros((64, 64), dtype=float);

hough_line_transform(I, H)
H = non_max_supressoin(H, 2)
lines = extract_lines(H)
print(lines)

H = H * 255/H.max()

im_out = Image.fromarray(np.uint8(H * 255.0), mode="L")
im_out.show()
 
