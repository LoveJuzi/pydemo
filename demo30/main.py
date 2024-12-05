#!/usr/bin/python3

from utils import gcd

import math


###############################################################################
def add(x, y):
    return Arithmetic.add(x, y)


def sub(x, y):
    return Arithmetic.sub(x, y)


def mul(x, y):
    return Arithmetic.mul(x, y)


def div(x, y):
    return Arithmetic.div(x, y)


###############################################################################
class Arithmetic:
    add_funcs = {}

    @staticmethod
    def install_add_func(k, v):
        Arithmetic.add_funcs[k] = v

    @staticmethod
    def add(x, y):
        k = Arithmetic.get_key(x, y)
        if k not in Arithmetic.add_funcs:
            # ERROR
            return None
        return Arithmetic.add_funcs[k](x, y)

    sub_funcs = {}

    @staticmethod
    def install_sub_func(k, v):
        Arithmetic.sub_funcs[k] = v

    @staticmethod
    def sub(x, y):
        k = Arithmetic.get_key(x, y)
        if k not in Arithmetic.sub_funcs:
            # ERROR
            return None
        return Arithmetic.sub_funcs[k](x, y)

    mul_funcs = {}

    @staticmethod
    def install_mul_func(k, v):
        Arithmetic.mul_funcs[k] = v

    @staticmethod
    def mul(x, y):
        k = Arithmetic.get_key(x, y)
        if k not in Arithmetic.mul_funcs:
            # ERROR
            return None
        return Arithmetic.mul_funcs[k](x, y)

    div_funcs = {}

    @staticmethod
    def install_div_func(k, v):
        Arithmetic.div_funcs[k] = v

    @staticmethod
    def div(x, y):
        k = Arithmetic.get_key(x, y)
        if k not in Arithmetic.div_funcs:
            # ERROR
            return None
        return Arithmetic.div_funcs[k](x, y)

    @staticmethod
    def get_key(x, y):
        xtype = x.ari_type()
        ytype = y.ari_type()
        return (xtype, ytype)


###############################################################################
class ComplexOp:
    @staticmethod
    def add(z1, z2):
        REAL = z1.real_part() + z2.real_part()
        IMAG = z1.imag_part() + z2.imag_part()
        return ComplexFactory.make("Rectangular", REAL, IMAG)

    @staticmethod
    def sub(z1, z2):
        REAL = z1.real_part() - z2.real_part()
        IMAG = z1.imag_part() - z2.imag_part()
        return ComplexFactory.make("Rectangular", REAL, IMAG)

    @staticmethod
    def mul(z1, z2):
        MAG = z2.magnitude() * z2.magnitude()
        ANGLE = z2.angle() + z2.angle()
        return ComplexFactory.make("Polar", MAG, ANGLE)

    @staticmethod
    def div(z1, z2):
        MAG = z1.magnitude() / z2.magnitude()
        ANGLE = z1.angle() - z2.angle()
        return ComplexFactory.make("Polar", MAG, ANGLE)


Arithmetic.install_add_func(("Complex", "Complex"), ComplexOp.add)
Arithmetic.install_sub_func(("Complex", "Complex"), ComplexOp.sub)
Arithmetic.install_mul_func(("Complex", "Complex"), ComplexOp.mul)
Arithmetic.install_div_func(("Complex", "Complex"), ComplexOp.div)


###############################################################################
class ComplexFactory:
    make_funcs = {}

    @staticmethod
    def install_make_func(k, v):
        ComplexFactory.make_funcs[k] = v

    @staticmethod
    def make(lable, x, y):
        if lable not in ComplexFactory.make_funcs:
            # TODO: ERROR
            return None
        return ComplexFactory.make_funcs[lable](x, y)


###############################################################################
class Complex:
    def __init__(self):
        super().__init__()

    def ari_type(self):
        return "Complex"


class ComplexRectangular(Complex):
    def __init__(self, real, imag):
        super().__init__()
        self._real = real
        self._imag = imag

    def real_part(self):
        return self._real

    def imag_part(self):
        return self._imag

    def magnitude(self):
        return math.sqrt(self.real_part() ** 2, self.imag_part() ** 2)

    def angle(self):
        return math.atan(self.imag_part(), self.real_part())


ComplexFactory.install_make_func("Rectangular", ComplexRectangular)


class ComplexPolar(Complex):
    def __init__(self, mag, ang):
        super().__init__()
        self._mag = mag
        self._ang = ang

    def real_part(self):
        return self.magnitude() * math.cos(self.angle())

    def imag_part(self):
        return self.magnitude() * math.sin(self.angle())

    def magnitude(self):
        return self._mag

    def angle(self):
        return self._ang


ComplexFactory.install_make_func("Polar", ComplexPolar)


###############################################################################
class RationalOp:
    @staticmethod
    def add(x, y):
        NUMER = x.numer() * y.denom() + y.numer() * x.denom()
        DENOM = x.denom() * y.denom()
        return Rational(NUMER, DENOM)

    @staticmethod
    def sub(x, y):
        NUMER = x.numer() * y.denom() - y.numer() * x.denom()
        DENOM = x.denom() * y.denom()
        return Rational(NUMER, DENOM)

    @staticmethod
    def mul(x, y):
        NUMER = x.numer(x) * y.numer(y)
        DENOM = x.denom(x) * y.denom(y)
        return Rational(NUMER, DENOM)

    @staticmethod
    def div(x, y):
        NUMER = x.numer(x) * y.denom(y)
        DENOM = x.denom(x) * y.numer(y)
        return Rational(NUMER, DENOM)

    @staticmethod
    def equal(x, y):
        return x.numer() * y.denom() == x.denom() * y.numer()


Arithmetic.install_add_func(("Rational", "Rational"), RationalOp.add)
Arithmetic.install_sub_func(("Rational", "Rational"), RationalOp.sub)
Arithmetic.install_mul_func(("Rational", "Rational"), RationalOp.mul)
Arithmetic.install_div_func(("Rational", "Rational"), RationalOp.div)


class Rational:
    def __init__(self, n, d):
        g = gcd(n, d)
        self._number = n // g
        self._denom = d // g

    def numer(self):
        return self._number

    def denom(self):
        return self._denom

    def print(self):
        return f"{self.numer() / self.denom()}"

    def ari_type(self):
        return "Rational"


###############################################################################
class IntegerOp:
    def add(x, y):
        return Integer(x.num() + y.num())

    def sub(x, y):
        return Integer(x.num() - y.num())

    def mul(x, y):
        return Integer(x.num() * y.num())

    def div(x, y):
        return Integer(x.num() // y.num())


Arithmetic.install_add_func(("Integer", "Integer"), IntegerOp.add)
Arithmetic.install_sub_func(("Integer", "Integer"), IntegerOp.sub)
Arithmetic.install_mul_func(("Integer", "Integer"), IntegerOp.mul)
Arithmetic.install_div_func(("Integer", "Integer"), IntegerOp.div)


class Integer:
    def __init__(self, num):
        self._num = num

    def num(self):
        return self._num

    def ari_type(self):
        return "Integer"


###############################################################################
class NumberOp:
    def add(x, y):
        return Number(x.num() + y.num())

    def sub(x, y):
        return Number(x.num() - y.num())

    def mul(x, y):
        return Number(x.num() * y.num())

    def div(x, y):
        return Number(x.num() / y.num())


Arithmetic.install_add_func(("Number", "Number"), NumberOp.add)
Arithmetic.install_sub_func(("Number", "Number"), NumberOp.sub)
Arithmetic.install_mul_func(("Number", "Number"), NumberOp.mul)
Arithmetic.install_div_func(("Number", "Number"), NumberOp.div)


class Number:
    def __init__(self, num):
        self._num = num

    def num(self):
        return self._num

    def ari_type(self):
        return "Number"


# test ########################################################################
def test_add_complex():
    z1 = ComplexFactory.make("Rectangular", 1, 2)
    z2 = ComplexFactory.make("Rectangular", 1, 2)
    z3 = add(z1, z2)
    assert z3.real_part() == 2
    assert z3.imag_part() == 4
