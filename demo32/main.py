#!/usr/bin/python3

from utils import pair, head, tail, llist, gcd

from utils import list_equal

import math


###############################################################################
def add(x, y):
    return Arithmetic.apply(Arithmetic.add, x, y)


def sub(x, y):
    return Arithmetic.apply(Arithmetic.sub, x, y)


def mul(x, y):
    return Arithmetic.apply(Arithmetic.mul, x, y)


def div(x, y):
    return Arithmetic.apply(Arithmetic.div, x, y)


def equal(x, y):
    return Arithmetic.apply(Arithmetic.equal, x, y)


def ari_print(x):
    return Arithmetic.apply(Arithmetic.print, x)


###############################################################################
class Arithmetic:
    convert_funcs = {}

    @staticmethod
    def install_convert_func(k, v):
        Arithmetic.convert_funcs[k] = v

    @staticmethod
    def convert(x, toType):
        k = (Arithmetic.get_type(x), toType)
        if k not in Arithmetic.convert_funcs:
            return None
        return Arithmetic.convert_funcs[k](x)

    @staticmethod
    def convert_param(x, y):
        t1 = Arithmetic.get_type(x)
        t2 = Arithmetic.get_type(y)
        if t1 == t2:
            return (x, y)
        x1 = Arithmetic.convert(x, t2)
        if x1 is not None:
            return (x1, y)
        y1 = Arithmetic.convert(y, t1)
        if y1 is not None:
            return (x, y1)
        return None

    @staticmethod
    def wrap_param(x):
        xt = type(x)
        if xt == int:
            return Integer(x)
        if xt == float:
            return Number(x)
        return x

    @staticmethod
    def apply(f, *args):
        wrap_args = [Arithmetic.wrap_param(arg) for arg in args]

        arg_cnt = len(args)
        if arg_cnt == 2:
            return Arithmetic.apply_2param(f, *wrap_args)

        return f(*wrap_args)

    @staticmethod
    def apply_2param(f, x, y):
        param = Arithmetic.convert_param(x, y)
        if param is None:
            # ERROR
            return None
        return f(param[0], param[1])

    @staticmethod
    def apply_2param_func(funcs, x, y):
        k = Arithmetic.get_key(x, y)
        if k not in funcs:
            # ERROR
            return None
        return funcs[k](x, y)

    add_funcs = {}

    @staticmethod
    def install_add_func(k, v):
        Arithmetic.add_funcs[k] = v

    @staticmethod
    def add(x, y):
        return Arithmetic.apply_2param_func(Arithmetic.add_funcs, x, y)

    sub_funcs = {}

    @staticmethod
    def install_sub_func(k, v):
        Arithmetic.sub_funcs[k] = v

    @staticmethod
    def sub(x, y):
        return Arithmetic.apply_2param_func(Arithmetic.sub_funcs, x, y)

    mul_funcs = {}

    @staticmethod
    def install_mul_func(k, v):
        Arithmetic.mul_funcs[k] = v

    @staticmethod
    def mul(x, y):
        return Arithmetic.apply_2param_func(Arithmetic.mul_funcs, x, y)

    div_funcs = {}

    @staticmethod
    def install_div_func(k, v):
        Arithmetic.div_funcs[k] = v

    @staticmethod
    def div(x, y):
        return Arithmetic.apply_2param_func(Arithmetic.div_funcs, x, y)

    equal_funcs = {}

    @staticmethod
    def install_equal_func(k, v):
        Arithmetic.equal_funcs[k] = v

    @staticmethod
    def equal(x, y):
        return Arithmetic.apply_2param_func(Arithmetic.equal_funcs, x, y)

    print_funcs = {}

    @staticmethod
    def install_print_func(k, v):
        Arithmetic.print_funcs[k] = v

    @staticmethod
    def print(x):
        k = Arithmetic.get_type(x)
        if k not in Arithmetic.print_funcs:
            # ERROR
            return None
        return Arithmetic.print_funcs[k](x)

    @staticmethod
    def get_key(x, y):
        xtype = x.ari_type()
        ytype = y.ari_type()
        return (xtype, ytype)

    @staticmethod
    def get_type(x):
        return x.ari_type()


###############################################################################
class ComplexOp:
    @staticmethod
    def add(z1, z2):
        REAL = z1.real_part() + z2.real_part()
        IMAG = z1.imag_part() + z2.imag_part()
        return Complex("Rectangular", REAL, IMAG)

    @staticmethod
    def sub(z1, z2):
        REAL = z1.real_part() - z2.real_part()
        IMAG = z1.imag_part() - z2.imag_part()
        return Complex("Rectangular", REAL, IMAG)

    @staticmethod
    def mul(z1, z2):
        MAG = z2.magnitude() * z2.magnitude()
        ANGLE = z2.angle() + z2.angle()
        return Complex("Polar", MAG, ANGLE)

    @staticmethod
    def div(z1, z2):
        MAG = z1.magnitude() / z2.magnitude()
        ANGLE = z1.angle() - z2.angle()
        return Complex("Polar", MAG, ANGLE)

    @staticmethod
    def equal(z1, z2):
        return z1.real_part() == z2.real_part() and z1.imag_part() == z2.imag_part()

    @staticmethod
    def print(z):
        return z.print()


Arithmetic.install_add_func(("Complex", "Complex"), ComplexOp.add)
Arithmetic.install_sub_func(("Complex", "Complex"), ComplexOp.sub)
Arithmetic.install_mul_func(("Complex", "Complex"), ComplexOp.mul)
Arithmetic.install_div_func(("Complex", "Complex"), ComplexOp.div)
Arithmetic.install_equal_func(("Complex", "Complex"), ComplexOp.equal)
Arithmetic.install_print_func("Complex", ComplexOp.print)


###############################################################################
class Complex:
    def __init__(self, label, x, y):
        super().__init__()
        self._complex = ComplexFactory.make(label, x, y)

    def real_part(self):
        return self._complex.real_part()

    def imag_part(self):
        return self._complex.imag_part()

    def magnitude(self):
        return self._complex.magnitude()

    def angle(self):
        return self._complex.angle()

    def print(self):
        return self._complex.print()

    def ari_type(self):
        return "Complex"


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


class ComplexRectangular:
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

    def print(self):
        return f"{self.real_part()} + i{self.imag_part()}"


ComplexFactory.install_make_func("Rectangular", ComplexRectangular)


class ComplexPolar:
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

    def print(self):
        return f"{self.real_part()} + i{self.imag_part()}"


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

    @staticmethod
    def print(x):
        return x.print()


Arithmetic.install_add_func(("Rational", "Rational"), RationalOp.add)
Arithmetic.install_sub_func(("Rational", "Rational"), RationalOp.sub)
Arithmetic.install_mul_func(("Rational", "Rational"), RationalOp.mul)
Arithmetic.install_div_func(("Rational", "Rational"), RationalOp.div)
Arithmetic.install_equal_func(("Rational", "Rational"), RationalOp.equal)
Arithmetic.install_print_func("Rational", RationalOp.print)


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
    @staticmethod
    def add(x, y):
        return Integer(x.num() + y.num())

    @staticmethod
    def sub(x, y):
        return Integer(x.num() - y.num())

    @staticmethod
    def mul(x, y):
        return Integer(x.num() * y.num())

    @staticmethod
    def div(x, y):
        if x % y == 0:
            return Integer(x.num() // y.num())
        return Rational(x, y)

    @staticmethod
    def equal(x, y):
        return x.num() == y.num()

    @staticmethod
    def print(x):
        return x.print()


Arithmetic.install_add_func(("Integer", "Integer"), IntegerOp.add)
Arithmetic.install_sub_func(("Integer", "Integer"), IntegerOp.sub)
Arithmetic.install_mul_func(("Integer", "Integer"), IntegerOp.mul)
Arithmetic.install_div_func(("Integer", "Integer"), IntegerOp.div)
Arithmetic.install_equal_func(("Integer", "Integer"), IntegerOp.equal)
Arithmetic.install_print_func("Integer", IntegerOp.print)


class Integer:
    def __init__(self, num):
        self._num = num

    def num(self):
        return self._num

    def ari_type(self):
        return "Integer"

    def print(self):
        return f"{self.num()}"


###############################################################################
class NumberOp:
    @staticmethod
    def add(x, y):
        return Number(x.num() + y.num())

    @staticmethod
    def sub(x, y):
        return Number(x.num() - y.num())

    @staticmethod
    def mul(x, y):
        return Number(x.num() * y.num())

    @staticmethod
    def div(x, y):
        return Number(x.num() / y.num())

    @staticmethod
    def equal(x, y):
        return x.num() == y.num()

    @staticmethod
    def print(x):
        return x.print()


Arithmetic.install_add_func(("Number", "Number"), NumberOp.add)
Arithmetic.install_sub_func(("Number", "Number"), NumberOp.sub)
Arithmetic.install_mul_func(("Number", "Number"), NumberOp.mul)
Arithmetic.install_div_func(("Number", "Number"), NumberOp.div)
Arithmetic.install_equal_func(("Number", "Number"), NumberOp.equal)
Arithmetic.install_print_func("Number", NumberOp.print)


class Number:
    def __init__(self, num):
        self._num = num

    def num(self):
        return self._num

    def ari_type(self):
        return "Number"

    def print(self):
        return f"{self.num()}"


###############################################################################
class PolynomialOp:
    @staticmethod
    def add(p1, p2):
        if not PolynomialOp.equal_variable(p1.variable(), p2.variable()):
            # ERROR
            return None
        return Polynomial(
            PolynomialOp.get_variable(p1, p2),
            PolynomialOp.add_terms(p1.term_list(), p2.term_list()),
        )

    @staticmethod
    def mul(p1, p2):
        pass

    @staticmethod
    def equal(p1, p2):
        if not PolynomialOp.equal_variable(p1.variable(), p2.variable()):
            return False
        return PolynomialOp.equal_terms(p1.term_list(), p2.term_list())

    @staticmethod
    def print(p):
        return p.print()

    @staticmethod
    def add_terms(tlist1, tlist2):
        if tlist1 is None:
            return tlist2
        if tlist2 is None:
            return tlist1
        item1 = head(tlist1)
        item2 = head(tlist2)
        if item1.th() < item2.th():
            return (item2, PolynomialOp.add_terms(tlist1, tail(tlist2)))

        if item1.th() > item2.th():
            return (item1, PolynomialOp.add_terms(tail(tlist1), tlist2))

        coeff = add(item1.coeff(), item2.coeff())
        return pair(
            PolynomialTerm(item1.th(), coeff),
            PolynomialOp.add_terms(tail(tlist1), tail(tlist2)),
        )

    @staticmethod
    def equal_variable(v1, v2):
        if v1 == "":
            return True
        if v2 == "":
            return True
        return v1 == v2

    @staticmethod
    def get_variable(p1, p2):
        if p1.variable() == "":
            return p2.variable()
        return p1.variable()

    @staticmethod
    def equal_terms(tlist1, tlist2):
        return list_equal(tlist1, tlist2, PolynomialOp.equal_term)

    @staticmethod
    def equal_term(term1, term2):
        if not equal(term1.th(), term2.th()):
            return False
        return equal(term1.coeff(), term2.coeff())


Arithmetic.install_add_func(("Polynomial", "Polynomial"), PolynomialOp.add)
Arithmetic.install_mul_func(("Polynomial", "Polynomial"), PolynomialOp.mul)
Arithmetic.install_equal_func(("Polynomial", "Polynomial"), PolynomialOp.equal)
Arithmetic.install_print_func("Polynomial", PolynomialOp.print)


class Polynomial:
    def __init__(self, variable, term_list):
        self._variable = variable
        self._term_list = term_list

    def variable(self):
        return self._variable

    def term_list(self):
        return self._term_list

    def print(self):
        return f"[{self.variable()} {self.print_term_list(self.term_list())}]"

    # return f"{self.variable()}"

    def print_term_list(self, term_list):
        if term_list is None:
            return None

        if tail(term_list) is None:
            return f"{head(term_list).print()}"

        return f"{head(term_list).print()} {self.print_term_list(tail(term_list))}"

    def ari_type(self):
        return "Polynomial"


class PolynomialTerm:
    def __init__(self, th, coeff):
        self._th = th
        self._coeff = coeff

    def th(self):
        return self._th

    def coeff(self):
        return self._coeff

    def print(self):
        return f"{(ari_print(self.th()), ari_print(self.coeff()))}"


###############################################################################


class NumberToComplex:
    @staticmethod
    def convert(x):
        return Complex("Rectangular", x.num(), 0)


Arithmetic.install_convert_func(("Number", "Complex"), NumberToComplex.convert)


class RationalToNumber:
    @staticmethod
    def convert(x):
        return Number(x.numer() / x.denom())


Arithmetic.install_convert_func(("Rational", "Number"), RationalToNumber.convert)


class RationalToComplex:
    @staticmethod
    def convert(x):
        return NumberToComplex.convert(RationalToNumber.convert(x))


Arithmetic.install_convert_func(("Rational", "Complex"), RationalToComplex.convert)


class IntegerToRational:
    @staticmethod
    def convert(x):
        return Rational(x.num(), 1)


Arithmetic.install_convert_func(("Integer", "Rational"), IntegerToRational.convert)


class IntegerToNumber:
    @staticmethod
    def convert(x):
        return RationalToNumber.convert(IntegerToRational.convert(x))


Arithmetic.install_convert_func(("Integer", "Number"), IntegerToNumber.convert)


class IntegerToComplex:
    @staticmethod
    def convert(x):
        return NumberToComplex.convert(IntegerToNumber.convert(x))


Arithmetic.install_convert_func(("Integer", "Complex"), IntegerToComplex.convert)


class ConstToPolynomial:
    @staticmethod
    def convert(x):
        return Polynomial("", llist(PolynomialTerm(0, x)))


Arithmetic.install_convert_func(("Complex", "Polynomial"), ConstToPolynomial.convert)
Arithmetic.install_convert_func(("Rational", "Polynomial"), ConstToPolynomial.convert)
Arithmetic.install_convert_func(("Number", "Polynomial"), ConstToPolynomial.convert)
Arithmetic.install_convert_func(("Integer", "Polynomial"), ConstToPolynomial.convert)


# test ########################################################################
def test_add_complex():
    z1 = Complex("Rectangular", 1, 2)
    z2 = Complex("Rectangular", 1, 2)
    z3 = add(z1, z2)
    assert z3.real_part() == 2
    assert z3.imag_part() == 4


def test_add_int():
    d = add(1, 2)
    assert d.num() == 3


def test_equal_int():
    assert equal(1, 1)


def test_equal_number():
    assert equal(1.0, 1)


def test_equal_ratioanl():
    assert equal(Rational(1, 1), Rational(1, 1))


def test_equal_complex():
    assert equal(Complex("Rectangular", 0, 1), Complex("Rectangular", 0, 1))


def test_equal_polynomial():
    assert equal(
        Polynomial("x", llist(PolynomialTerm(1, 1))),
        Polynomial("x", llist(PolynomialTerm(1, 1))),
    )

    assert not equal(
        Polynomial("x", llist(PolynomialTerm(1, 2))),
        Polynomial("x", llist(PolynomialTerm(1, 1))),
    )


def test_add_poly():
    p1 = Polynomial("x", llist(PolynomialTerm(2, 1), PolynomialTerm(1, 3)))
    p2 = Polynomial("x", llist(PolynomialTerm(2, 1), PolynomialTerm(1, 3)))
    assert equal(p1, p2)
    p3 = add(p1, p2)
    p4 = Polynomial("x", llist(PolynomialTerm(2, 2), PolynomialTerm(1, 6)))
    assert equal(p3, p4)


def test_add_poly_integer():
    p1 = Polynomial("x", llist(PolynomialTerm(2, 1), PolynomialTerm(1, 3)))
    p2 = 2
    p3 = add(p1, p2)
    p4 = Polynomial(
        "x",
        llist(
            PolynomialTerm(2, 1),
            PolynomialTerm(1, 3),
            PolynomialTerm(0, Integer(2)),
        ),
    )
    assert equal(p3, p4)
