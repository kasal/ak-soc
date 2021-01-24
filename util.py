#!/bin/python

# greatest common divisor (Czech: nsd)
# Euclidean algorith (Czech: EAPD)
def nsd(x):
    assert isinstance(x, list)
    assert len(x) >= 2
    a,b = x[:2]
    if a < b:
        a,b = b,a
    assert b <= a
    assert b > 0
    while (b > 0):
        a, b = b, a % b
    if len(x) == 2:
        return a
    else:
        return nsd([a] + x[2:])

# least common multiple (Czech: nsn)
# gcd * lcm = a * b (Czech: nsd * nsn = a * b)
#
def nsn(x):
    assert isinstance(x, list)
    if (len(x) == 1):
        return x[0]
    assert len(x) >= 2
    a = x[0] * x[1] // nsd(x[:2])
    if len(x) == 2:
        return a
    else:
        return nsn([a] + x[2:])

# check if two sequences are equivalent
#
# equivalent means that they are the same up to a rotation
#
def are_equal(x, y):
    if (len(x) != len(y)):
        return False
    for i in range(len(x)):
        # the first check is redundant, but might speed things up...
        if x[i] == y[0] and x[i:] + x[:i] == y:
            return True
    return False
