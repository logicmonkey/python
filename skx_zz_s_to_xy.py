# Zig Zag space filling curve xy to s mapping for a W*W region
#
# Define diagonals as the sum of the x and y coordinates since it is a
# constant. To the right of the main diagonal the calculation needs to be
# aware of the region width, so the function call uses -x and -y to achieve
# a 180 degree flip (effectively along that main diagonal)
# Algorithm does not require a region to be anything other than just square.

import math

ORDER = 4

def tri(n):
    return int(n*(n+1)/2) # Triangular number starts a diagonal

def tri_root(n):
    return int((math.sqrt(8*n+1)-1)/2)

def zz_s_to_xy(s, r): # distance s, reflection
    tr = tri_root(s)
    t = tri(tr) # nearest triangular number less than or equal to s
    d = s-t     # distance from the triangular start of diagonal
    if tr%2:    # check if the diagonal is an odd or even one
        if r:
            return ORDER-1-d, ORDER-1-tr+d
        else:
            return d, tr-d
    else:
        if r:
            return ORDER-1-tr+d, ORDER-1-d
        else:
            return tr-d, d

def zigzag_s_to_xy(s, ORDER):
    if (s<ORDER*ORDER/2): # left of main diagonal
        return zz_s_to_xy(s, 0)
    else:                 # right of main diagonal: reflect
        return zz_s_to_xy(ORDER**2-1-s, 1)


for s in range(0, ORDER*ORDER):
    x, y = zigzag_s_to_xy(s, ORDER)
    print("{:3d} {:3d} {:3d}".format(s,x,y))
