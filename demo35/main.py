#!/usr/bin/python3

from utils import CONS, CAR, CDR, LIST


##########################################################################################
def make_rat(n, d):
    return CONS(n, d)


def numer(x):
    return CAR(x)


def denom(x):
    return CDR(x)


def add_rat(x, y):
    p11 = numer(x)
    p12 = denom(x)
    p21 = numer(y)
    p22 = denom(y)
    return make_rat(p11 * p22 + p12 * p21, p12 * p22)


def equal_rat(x, y):
    return numer(x) * denom(y) == denom(x) * numer(y)


def RAT(n, d):
    rat = CONS(n, d)

    def numer():
        return CAR(rat)

    def denom():
        return CDR(rat)

    def dispatch(tag):
        if tag == "numer":
            return numer()
        if tag == "denom":
            return denom()

    return dispatch


def RAT_OP_FUNC():
    def add(rat1, rat2):
        return RAT(
            CALL(rat1, "numer") * CALL(rat2, "denom")
            + CALL(rat2, "numer") * CALL(rat1, "denom"),
            CALL(rat1, "denom") * CALL(rat2, "denom"),
        )

    def equal(rat1, rat2):
        return CALL(rat1, "numer") * CALL(rat2, "denom") == CALL(rat1, "denom") * CALL(
            rat2, "numer"
        )

    def dispatch(tag, *args):
        if tag == "add":
            return add(*args)
        if tag == "equal":
            return equal(*args)

    return dispatch


RAT_OP = RAT_OP_FUNC()


def CALL(obj, method, *args):
    return obj(method, *args)


def EQUAL_RAT(rat1, rat2):
    return CALL(rat1, "numer") * CALL(rat2, "denom") == CALL(rat1, "denom") * CALL(
        rat2, "numer"
    )


##########################################################################################
def test_add_rat():
    rat1 = make_rat(1, 2)
    rat2 = make_rat(1, 2)
    assert equal_rat(add_rat(rat1, rat2), make_rat(1, 1))


def test_RAT():
    rat1 = RAT(1, 2)
    rat2 = RAT(1, 2)
    assert EQUAL_RAT(rat1, rat2)
    assert CALL(RAT_OP, "equal", CALL(RAT_OP, "add", rat1, rat2), RAT(1, 1))
