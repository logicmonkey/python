# Zig Zag space filling curve xy to s mapping for a W*W region
#
# Define diagonals as the sum of the x and y coordinates since it is a
# constant. To the right of the main diagonal the calculation needs to be
# aware of the region width, so the function call uses -x and -y to achieve
# a 180 degree flip (effectively along that main diagonal)
# Algorithm does not require a region to be anything other than just square.

N = 5

import math
STAGES = int(math.log(N,2))+1

def isqrt_pipe(arem, aval, stage):
    one = 1 << 2*stage
    cmp = aval | one

    yrem = arem
    yval = aval >> 1
    if arem >= cmp:
        yrem = yrem - cmp
        yval = yval | one
    return yrem, yval

def isqrt(n):
    rem = n
    val = 0
    for ps in reversed(range(0, STAGES+1)):
        rem, val = isqrt_pipe(rem, val, ps)
    return val

def tri(n):
    return (n*(n+1))>>1 # Triangular number starts a diagonal

def tri_root(n):
    return (isqrt(n<<3|1)-1)>>1

def zz_s_to_xy(s, rpd): # distance s, right of principal diagonal
    if rpd:
        s = N*N-1 - s
        xt, yt = N-1, N-1
    tr = tri_root(s)
    t = tri(tr) # nearest triangular number less than or equal to s
    d = s-t     # distance from the triangular start of diagonal

    if tr%2:    # check if the diagonal is an odd or even one
        if rpd: # right of principal diagonal
            return xt-d, yt-tr+d
        else:
            return d, tr-d
    else:
        if rpd:
            return xt-tr+d, yt-d
        else:
            return tr-d, d

def zigzag_s_to_xy(s):
    if s<N*N/2: # left of principal diagonal
        return zz_s_to_xy(s, False)
    else:         # right of principal diagonal: reflect
        return zz_s_to_xy(s, True)

for s in range(0, N*N):
    x, y = zigzag_s_to_xy(s)
    print("{:3d} {:3d} {:3d}".format(s,x,y))
