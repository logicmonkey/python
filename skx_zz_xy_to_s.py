# Zig Zag space filling curve xy to s mapping for a W*W region
#
# Define diagonals as the sum of the x and y coordinates since it is a
# constant. To the right of the main diagonal the calculation needs to be
# aware of the region width, so the function call uses -x and -y to achieve
# a 180 degree flip (effectively along that main diagonal)
# Algorithm does not require a region to be anything other than just square.

N = 5

def tri(n):
    return (n*(n+1))>>1 # Triangular number starts a diagonal

def zz_xy_to_s(x, y):
    if (x+y)%2:
        return tri(x+y) + x # for diagonals going up and right
    else:
        return tri(x+y) + y # for diagonals going down and left

def zigzag_xy_to_s(x, y):
    if (x+y<N): # left of main diagonal
        END = 0
        K = 1
        xt = x
        yt = y
    else:       # right of main diagonal: reflect
        END = N*N-1
        K = -1
        xt = N-1-x
        yt = N-1-y

    # distance s is purely a function of N, x and y
    return END + K*zz_xy_to_s(xt, yt)

for y in range(0, N):
    for x in range(0, N):
        s = zigzag_xy_to_s(x, y)
        print("{:3d} ".format(s), end='')
    print("")
