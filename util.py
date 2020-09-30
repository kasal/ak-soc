#!/bin/python

# EAPD
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

# nsd * nsn = a * b
def nsn(x):
    assert isinstance(x, list)
    assert len(x) >= 2
    a = x[0] * x[1] // nsd(x[:2])
    if len(x) == 2:
        return a
    else:
        return nsn([a] + x[2:])
