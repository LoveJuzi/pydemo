#!/usr/bin/python3

# BASE ###################################################################################
NIL = None


def CONS(a, b):
    return [a, b]


def CAR(p):
    return p[0]


def CDR(p):
    return p[1]


def LIST(*args):
    if not args:
        return NIL
    return CONS(args[0], LIST(*args[1:]))
