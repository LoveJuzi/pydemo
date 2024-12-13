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


###############################################################################
def llist(*args):
    if not args:
        return None
    first_arg, *remain_args = args
    return pair(first_arg, llist(*remain_args))


def list_equal(l1, l2, equal_func):
    if l1 == l2:
        return True

    if l1 is None:
        return False
    if l2 is None:
        return False

    if not equal_func(head(l1), head(l2)):
        return False

    return list_equal(tail(l1), tail(l2), equal_func)


def test_list_equal():
    l1 = llist(1, 2)
    l2 = llist(1, 2)
    assert list_equal(l1, l2, lambda x, y: x == y)
