#!/usr/bin/env python

# Euclid's algorithm

# compare exchange ensures p/q < 1/1
#
def cex(a):
    if a[0] > a[1]:
        return (a[1], a[0])
    else:
        return a

# recurse until no remainder
#
def gcd(a):
    r = a[1] % a[0]
    if r == 0:
        return a[0]
    else:
        return gcd((r, a[0])) # remainder is new divisor

t = (5940, 2160)
print(gcd(cex(t)))

print(gcd(cex((182664, 154875))))
print(gcd(cex((gcd(cex((182664, 154875))), 137688)))) # i'm not proud of this bit :)
