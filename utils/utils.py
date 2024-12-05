#!/usr/bin/python3


###############################################################################
def pair(x, y):
    return (x, y)


def head(p):
    return p[0]


def tail(p):
    return p[1]


###############################################################################
def mutable_pair(x, y):
    return [x, y]


def set_head(p, x):
    p[0] = x
    return p


def set_tail(p, y):
    p[1] = y
    return p


###############################################################################
def gcd(a, b):
    if a % b == 0:
        return b
    return gcd(b, a % b)
