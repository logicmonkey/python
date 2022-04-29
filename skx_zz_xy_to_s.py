# Zig Zag space filling curve xy to s mapping for a W*W region
#
# Define diagonals as the sum of the x and y coordinates since it is a
# constant. To the right of the main diagonal the calculation needs to be
# aware of the region width, so the function call uses -x and -y to achieve
# a 180 degree flip (effectively along that main diagonal)
# Algorithm does not require a region to be anything other than just square.

ORDER = 4

def tri(n):
    return int(n*(n+1)/2) # Triangular number starts a diagonal

def zz_xy_to_s(x, y):
    # Even and odd diagonals increment in different directions
    if (x+y)%2:
        return tri(x+y) + x # for diagonals going up and right
    else:
        return tri(x+y) + y # for diagonals going down and left


def zigzag_xy_to_s(x, y, ORDER):
    if (x+y<ORDER): # left of main diagonal
        N = 0
        K = 1
        xt = x
        yt = y
    else:       # right of main diagonal: reflect
        N = ORDER*ORDER-1
        K = -1
        xt = ORDER-1 -x
        yt = ORDER-1 -y

    # distance s is purely a function of W, x and y
    return  N + K*zz_xy_to_s(xt, yt)

for y in range(0, ORDER):
    for x in range(0, ORDER):

        s = zigzag_xy_to_s(x, y, ORDER)
        print("{:3d} ".format(s), end='')
    print("")
