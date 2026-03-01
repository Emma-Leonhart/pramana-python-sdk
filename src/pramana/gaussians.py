"""Gaussian Integer & Rational Number Classes

A Gaussian integer is a complex number whose real and imaginary parts are both integers.
Similarly, a Gaussian rational is a complex number whose real and imaginary parts are
rational numbers.

In mathematics, Gaussian integers and rationals are denoted by Z[i] & Q[i], resp.
In Pramana, these are called Gint and Gauss, respectively.

The classes support the arithmetic of Gaussian integers and rationals using the
operators: +, -, *, /, //, %, **, +=, -=, *=, and /=, along with a modified version
of divmod, modified_divmod, and two functions related to the Greatest Common Divisor:
gcd and xgcd.

Example:
  > from pramana import Gint, Gauss
  >
  > alpha = Gint(11, 3)
  > beta = Gint(1, 8)
  > a, x, y = Gint.xgcd(alpha, beta)
  > print(f"{alpha * x + beta * y} = {alpha} * {x} + {beta} * {y}")
  > (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j

Original implementation:
  Copyright (C) 2024 Alfred J. Reich, Ph.D. <al.reich@gmail.com>
  Source: https://github.com/alreich/gaussian_integers
  License: MIT

  Forked into the Pramana Python SDK and refactored: classes renamed from
  Zi/Qi to Gint/Gauss per Pramana naming conventions. The original Zi and Qi
  names are preserved as aliases. See NOTICE.md for full attribution.
"""

__original_author__ = "Alfred J. Reich, Ph.D."
__original_contact__ = "al.reich@gmail.com"
__original_copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__original_license__ = "MIT"
__original_version__ = "1.0.0"
__original_source__ = "https://github.com/alreich/gaussian_integers"

import builtins
import math
import uuid
from fractions import Fraction
from numbers import Complex
from random import randint
from functools import wraps

PRAMANA_NAMESPACE = uuid.UUID("a6613321-e9f6-4348-8f8b-29d2a3c86349")


def to_gaussian_rational(number):
    """Given a number, return its equivalent Gaussian rational (Gauss)."""
    if isinstance(number, (int, float, complex, Gint, Fraction)):
        return Gauss(number)
    elif isinstance(number, Gauss):
        return number
    else:
        raise TypeError(f"'{number}' cannot be cast into a Gaussian rational")


def gaussian_rational(fnc):
    """For use as a decorator that casts an argument into a Gaussian rational."""
    @wraps(fnc)
    def gaussian_rational_wrapper(arg, num):
        qi = to_gaussian_rational(num)
        return fnc(arg, qi)
    return gaussian_rational_wrapper


class Gint:
    """Gaussian Integer (Z[i]) with arithmetic and number-theoretic functionality.

    A Gaussian integer has two integer components, re & im, representing re + im*i.
    Floats and complex numbers can be entered, but they will be rounded to the
    nearest integers. If a complex number is provided for re, then the value of
    im will be ignored. Additionally, the complex number's components, real & imag,
    will be rounded to the nearest integers and used as inputs for re & im, resp.
    """

    def __init__(self, re=None, im=None):
        if isinstance(re, (float, int)):
            self.__re = round(re)
            if im is None:
                self.__im = 0
            elif isinstance(im, (float, int)):
                self.__im = round(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif isinstance(re, complex):
            if im is None:
                self.__re = round(re.real)
                self.__im = round(re.imag)
            elif isinstance(im, (complex, Gint)):
                self.__re = Gint(re)
                self.__im = Gint(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif isinstance(re, Gint):
            if im is None:
                self.__re = re.real
                self.__im = re.imag
            elif isinstance(im, (complex, Gint)):
                self.__re = Gint(re)
                self.__im = Gint(im)
            else:
                raise Exception(f"Inputs incompatible: {re} and {im}")
        elif re is None:
            if im is None:
                self.__re = 0
                self.__im = 0
            else:
                raise Exception("If re is None, then im must be None. But im = {im}")
        else:
            raise Exception("We should never get to this point in the code")

    @property
    def real(self):
        return self.__re

    @property
    def imag(self):
        return self.__im

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"Gint({self.real})"
        else:
            return f"Gint({self.real}, {self.imag})"

    def __str__(self) -> str:
        re, im = self.real, self.imag
        if im == 0:
            return str(re)
        im_part = "i" if im == 1 else "-i" if im == -1 else f"{im}i"
        if re == 0:
            return im_part
        sign = " + " if im > 0 else " - "
        abs_im_part = "i" if abs(im) == 1 else f"{abs(im)}i"
        return f"{re}{sign}{abs_im_part}"

    # NOTE: Python ints and floats have both 'real' and 'imag' properties, so
    # no conversion to Gaussian integers is necessary to use them in the arithmetic
    # operations, below.

    def __add__(self, other):
        """Implements the + operator: self + other"""
        return Gint(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self"""
        return Gint(other) + self

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        return Gint(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        """Implements the subtraction operator: self - other"""
        return Gint(self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self"""
        return Gint(other) - self

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        return Gint(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other"""
        if isinstance(other, Gauss):
            return Gauss(self) * other
        else:
            a = self.real
            b = self.imag
            c = round(other.real)
            d = round(other.imag)
            return Gint(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        """The reflected (swapped) operand for multiplication: other * self"""
        return Gint(other) * self

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        c = round(other.real)
        d = round(other.imag)
        return Gint(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):
        """Implements the ** operator: self ** n.

        If n == 0, then Gint(1, 0) is returned. If n < 0, then the Gaussian
        rational, Gauss, for 1 / self**n is returned. Otherwise, self ** n is returned.
        """
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Gint(1)  # "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:  # n < 0
                result = 1 / (self ** abs(n))
        return result

    def __complex__(self) -> complex:
        """Return the complex number that corresponds to this Gint."""
        return complex(self.real, self.imag)

    def __neg__(self):
        """Negate this Gint."""
        return Gint(-self.real, -self.imag)

    def __eq__(self, other: Complex) -> bool:
        """Return True if this Gint equals other."""
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        """Return True if this Gint does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    @gaussian_rational
    def __truediv__(self, other):  # self / other
        """Divide self by other, exactly, and return the resulting Gauss or Gint.

        The divisor (other) is first cast into a Gaussian rational (Gauss) prior to division.
        """
        return Gauss(self) / other  # Could still output a Gint

    @gaussian_rational
    def __rtruediv__(self, other):  # other / self
        """Divide other by self, exactly, and return the resulting Gauss or Gint.

        The dividend (other) is first cast into a Gaussian rational (Gauss) prior to division.
        """
        return other / Gauss(self)

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Gint, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Gint.
        """
        if isinstance(other, (int, float, complex, Gint)):
            return Gint(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Gint(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __mod__(self, other):
        """Implements the % operator.

        Returns the remainder of the result from modified_divmod
        """
        if isinstance(other, (int, float, complex)):
            oth = Gint(other)
        else:
            oth = other
        _, r = Gint.modified_divmod(self, oth)
        return r

    def __hash__(self):
        """Allow this Gint to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return math.sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, base):
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            other = Gint(other)
        if self.real != other.real:
            return self.real < other.real
        return self.imag < other.imag

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            other = Gint(other)
        if self.real != other.real:
            return self.real > other.real
        return self.imag > other.imag

    def __ge__(self, other):
        return self == other or self > other

    # --- Classification properties ---

    @property
    def is_real(self) -> bool:
        return self.imag == 0

    @property
    def is_purely_imaginary(self) -> bool:
        return self.real == 0 and self.imag != 0

    @property
    def is_zero(self) -> bool:
        return self.real == 0 and self.imag == 0

    @property
    def is_integer(self) -> bool:
        return self.imag == 0

    @property
    def is_gaussian_integer(self) -> bool:
        return True

    @property
    def is_one(self) -> bool:
        return self.real == 1 and self.imag == 0

    @property
    def is_positive(self) -> bool:
        return self.imag == 0 and self.real > 0

    @property
    def is_negative(self) -> bool:
        return self.imag == 0 and self.real < 0

    # --- Pramana identity ---

    @property
    def pramana_key(self) -> str:
        return f"{self.real},1,{self.imag},1"

    @property
    def pramana_id(self) -> str:
        canonical = f"{{{self.pramana_key}}}"
        return str(uuid.uuid5(PRAMANA_NAMESPACE, canonical))

    @property
    def pramana_url(self) -> str:
        return f"https://pramana.dev/entity/{self.pramana_id}"

    @property
    def pramana_label(self) -> str:
        return f"pra:num:{self.pramana_key}"

    @staticmethod
    def eye():
        """Return i = Gint(0, 1)"""
        return Gint(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Gints."""
        return [Gint(1), -Gint(1), Gint.eye(), -Gint.eye()]

    @property
    def is_unit(self):
        """Returns True if this Gint is a unit."""
        return self in Gint.units()

    @staticmethod
    def two():
        """Returns 1+i, because a Gaussian integer has an even norm if and only if
        it is a multiple of 1+i."""
        return Gint(1, 1)

    @property
    def conjugate(self):
        """Return the conjugate of this Gaussian integer"""
        return Gint(self.real, - self.imag)

    @property
    def norm(self) -> int:
        """Return the norm of this Gaussian integer.

        NOTE: The norm here is the square of the usual absolute value.
        """
        n = self * self.conjugate
        return n.real

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):
        """Return a random Gaussian integer with re1 <= re <= re2 and im1 <= im <= im2."""
        return Gint(randint(re1, re2), randint(im1, im2))

    def associates(self):
        """Return a list of this Gint's three associates"""
        us = Gint.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Gint is an associate of this Gint

        Otherwise, return False.
        """
        q = self // other
        if q:
            if q in Gint.units():
                return True
            else:
                return False
        else:
            return False

    def to_gaussian_rational(self):
        """Convert this Gaussian integer to an equivalent Gaussian rational."""
        return Gauss(self.real, self.imag)

    @staticmethod
    def norms_divide(a, b):
        """Divide the larger norm by the smaller norm. If they divide evenly,
        return the value; otherwise, if they don't divide evenly, return False."""
        x = a.norm
        y = b.norm
        sm = min(x, y)
        lg = max(x, y)
        if lg % sm == 0:
            return int(lg / sm)
        else:
            return False

    @staticmethod
    def from_array(arr):
        """Convert a two-element array into a Gaussian integer."""
        return Gint(int(arr[0]), int(arr[1]))

    # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    @staticmethod
    def modified_divmod(a, b):
        """The divmod algorithm, modified for Gaussian integers.

        Returns q & r, such that a = b * q + r, where
        r.norm < b.norm / 2. This is the Modified Division
        Theorem described in 'The Gaussian Integers' by Keith Conrad
        """
        q = Gint(complex(a * b.conjugate) / b.norm)  # Gint rounds the complex result here
        r = a - b * q
        return q, r

    @staticmethod
    def gcd(a, b, verbose=False):
        """A gcd algorithm for Gaussian integers.
        Returns the greatest common divisor of a & b.

        This function implements the Euclidean algorithm for Gaussian integers.
        """
        zero = Gint()
        if a * b == zero:
            raise ValueError(f"Both inputs must be non-zero: {a} and {b}")
        else:
            r1, r2 = a, b
            while r2 != zero:
                r0, r1 = r1, r2
                q, r2 = Gint.modified_divmod(r0, r1)
                if verbose:
                    print(f"   {r0} = {r1} * {q} + {r2}")
        return r1

    @staticmethod
    def xgcd(alpha, beta):
        """The Extended Euclidean Algorithm for Gaussian Integers.

        Three values are returned: gcd, x, & y, such that
        the Greatest Common Divisor (gcd) of alpha & beta can be
        written as gcd = alpha * x + beta * y. x & y are called
        Bezout's coefficients.
        """
        if isinstance(alpha, Gint) and isinstance(beta, Gint):
            zero = Gint()
        else:
            raise ValueError(f"Inputs must be two Gints.")

        # NOTE: Many of the lines below perform two assignment operations
        a, b = alpha, beta
        x, next_x = 1, 0
        y, next_y = 0, 1
        while b != zero:
            q = a // b
            next_x, x = x - q * next_x, next_x
            next_y, y = y - q * next_y, next_y
            a, b = b, a % b
        return a, x, y

    @staticmethod
    def congruent_modulo(a, b, c):
        """This method returns two values: The first value is True or False,
        depending on whether x is congruent to y modulo z;
        the second value is the result of computing (a - b) / c."""
        w = (a - b) / c
        if isinstance(w, Gint):
            return True, w
        else:
            return False, w

    @staticmethod
    def is_relatively_prime(a, b) -> bool:
        """Returns True if a and b are relatively prime, otherwise it returns false."""
        return Gint.gcd(a, b) in Gint.units()

    @staticmethod
    def is_gaussian_prime(x) -> bool:
        """Return True if x is a Gaussian prime.  Otherwise, return False.
        x can be an integer or a Gaussian integer (Gint).

        See https://mathworld.wolfram.com/GaussianPrime.html
        """
        re = im = norm = None

        if isinstance(x, Gint):
            re = abs(x.real)
            im = abs(x.imag)
            norm = x.norm
        elif isinstance(x, int):
            re = abs(x)
            im = 0
            norm = re * re

        if (re * im != 0) and isprime(norm):
            return True

        elif re == 0:
            if isprime(im) and (im % 4 == 3):
                return True
            else:
                return False

        elif im == 0:
            if isprime(re) and (re % 4 == 3):
                return True
            else:
                return False

        else:
            return False


Gint.ZERO = Gint(0, 0)
Gint.ONE = Gint(1, 0)
Gint.MINUS_ONE = Gint(-1, 0)
Gint.I = Gint(0, 1)


def isprime(n: int) -> bool:
    """Returns True if n is a positive, prime integer; otherwise, False is returned.

    Uses 6k±1 optimization for efficiency.
    """
    if not isinstance(n, int):
        return False
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


class Gauss:
    """Gaussian Rational (Q[i]) with exact fractional arithmetic.

    A Gaussian rational is a complex number whose real and imaginary parts
    are both rational numbers (fractions.Fraction). Supports full arithmetic
    with automatic type coercion from int, float, complex, Gint, and Fraction.
    """

    __max_denominator = 1_000_000

    def __init__(self, re=Fraction(0, 1), im=Fraction(0, 1)):

        if isinstance(re, Fraction):
            self.__real = re
        elif isinstance(re, (str, int, float)):
            self.__real = Fraction(re).limit_denominator(self.__max_denominator)
        elif isinstance(re, (complex, Gint)):
            self.__real = Fraction(re.real).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{re} is not a supported type")

        if isinstance(re, (complex, Gint)):
            self.__imag = Fraction(re.imag).limit_denominator(self.__max_denominator)
        elif isinstance(im, Fraction):
            self.__imag = im
        elif isinstance(im, (str, int, float)):
            self.__imag = Fraction(im).limit_denominator(self.__max_denominator)
        else:
            raise TypeError(f"{im} is not a supported type")

    @classmethod
    def max_denominator(cls):
        return cls.__max_denominator

    @classmethod
    def set_max_denominator(cls, value):
        if value > 1:
            cls.__max_denominator = value
            return cls.__max_denominator
        else:
            raise ValueError("max_denominator must be > 1")

    @property
    def real(self) -> Fraction:
        return self.__real

    @property
    def imag(self) -> Fraction:
        return self.__imag

    def __repr__(self):
        return f"Gauss({repr(str(self.real))}, {repr(str(self.imag))})"

    def __str__(self):
        if self.imag < 0:
            return f"({self.real}{self.imag}j)"
        else:
            return f"({self.real}+{self.imag}j)"

    @gaussian_rational
    def __add__(self, other):
        return Gauss(self.real + other.real, self.imag + other.imag)

    @gaussian_rational
    def __radd__(self, other):
        return other + self

    @gaussian_rational
    def __sub__(self, other):
        return Gauss(self.real - other.real, self.imag - other.imag)

    @gaussian_rational
    def __rsub__(self, other):
        return other - self

    @gaussian_rational
    def __mul__(self, other):
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        re = a * c - b * d
        im = a * d + b * c
        # Return a Gaussian integer if the denominators are 1
        if re.denominator == 1 and im.denominator == 1:
            return Gint(re.numerator, im.numerator)
        else:
            return Gauss(re, im)

    @gaussian_rational
    def __rmul__(self, other):
        return other * self

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Gauss(Fraction(1, 1), Fraction(0, 1))  # "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:  # n < 0
                result = 1 / self ** abs(n)
        return result

    @gaussian_rational
    def __truediv__(self, other):
        """Returns self/other as a Gaussian rational"""
        return self * other.inverse

    @gaussian_rational
    def __rtruediv__(self, other):
        """Returns other/self as a Gaussian rational"""
        return other * self.inverse

    def __neg__(self):
        return Gauss(-self.real, -self.imag)

    def __complex__(self) -> complex:
        return complex(float(self.real), float(self.imag))

    @gaussian_rational
    def __eq__(self, other: Complex) -> bool:
        """Test for equality."""
        return (self.real == other.real) and (self.imag == other.imag)

    @gaussian_rational
    def __ne__(self, other) -> bool:
        """Return True if this Gauss does NOT equal other."""
        return (self.real != other.real) or (self.imag != other.imag)

    def __hash__(self):
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        return math.sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, **kwargs):
        return NotImplemented

    def __lt__(self, other):
        other = to_gaussian_rational(other)
        if self.real != other.real:
            # Cross-multiply to compare: self.real.num * other.real.den vs other.real.num * self.real.den
            return self.real < other.real
        return self.imag < other.imag

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        other = to_gaussian_rational(other)
        if self.real != other.real:
            return self.real > other.real
        return self.imag > other.imag

    def __ge__(self, other):
        return self == other or self > other

    # --- Classification properties ---

    @property
    def is_real(self) -> bool:
        return self.imag == Fraction(0)

    @property
    def is_purely_imaginary(self) -> bool:
        return self.real == Fraction(0) and self.imag != Fraction(0)

    @property
    def is_zero(self) -> bool:
        return self.real == Fraction(0) and self.imag == Fraction(0)

    @property
    def is_integer(self) -> bool:
        return self.imag == Fraction(0) and self.real.denominator == 1

    @property
    def is_gaussian_integer(self) -> bool:
        return self.real.denominator == 1 and self.imag.denominator == 1

    @property
    def is_one(self) -> bool:
        return self.real == Fraction(1) and self.imag == Fraction(0)

    @property
    def is_positive(self) -> bool:
        return self.imag == Fraction(0) and self.real > 0

    @property
    def is_negative(self) -> bool:
        return self.imag == Fraction(0) and self.real < 0

    # --- Pramana identity ---

    @property
    def pramana_key(self) -> str:
        return f"{self.real.numerator},{self.real.denominator},{self.imag.numerator},{self.imag.denominator}"

    @property
    def pramana_id(self) -> str:
        canonical = f"{{{self.pramana_key}}}"
        return str(uuid.uuid5(PRAMANA_NAMESPACE, canonical))

    @property
    def pramana_url(self) -> str:
        return f"https://pramana.dev/entity/{self.pramana_id}"

    @property
    def pramana_label(self) -> str:
        return f"pra:num:{self.pramana_key}"

    # --- String formatting ---

    def to_raw_string(self) -> str:
        """Return <A,B,C,D> format."""
        r = self.real
        i = self.imag
        return f"<{r.numerator},{r.denominator},{i.numerator},{i.denominator}>"

    def to_improper_string(self) -> str:
        """Return improper fraction format like '7/2 + 1/4 i'."""
        re_str = str(self.real)
        im = self.imag
        if im == Fraction(0):
            return re_str
        abs_im = abs(im)
        im_str = "i" if abs_im == Fraction(1) else f"{abs_im}i"
        if self.real == Fraction(0):
            return im_str if im > 0 else f"-{im_str}"
        sign = " + " if im > 0 else " - "
        return f"{re_str}{sign}{im_str}"

    def to_mixed_string(self) -> str:
        """Return human-readable mixed fraction format like '3 & 1/2 + 1/4 i'."""
        def _mixed(f):
            if f.denominator == 1:
                return str(f.numerator)
            whole = int(f)
            remainder = abs(f - whole)
            if whole == 0:
                return str(f)
            if remainder == Fraction(0):
                return str(whole)
            sign = "-" if f < 0 else ""
            return f"{sign}{abs(whole)} & {remainder}"

        re_str = _mixed(self.real)
        im = self.imag
        if im == Fraction(0):
            return re_str
        abs_im = abs(im)
        abs_im_str = "i" if abs_im == Fraction(1) else f"{_mixed(abs_im)}i"
        if self.real == Fraction(0):
            if im > 0:
                return abs_im_str
            return f"-{abs_im_str}"
        sign = " + " if im > 0 else " - "
        return f"{re_str}{sign}{abs_im_str}"

    def to_decimal_string(self, precision=15) -> str:
        """Return decimal format like '3.5 + 0.25i'."""
        re_val = float(self.real)
        im_val = float(self.imag)

        def _fmt(v):
            if v == int(v):
                return str(int(v))
            return f"{v:.{precision}g}"

        re_str = _fmt(re_val)
        if im_val == 0:
            return re_str
        abs_im = abs(im_val)
        im_str = "i" if abs_im == 1.0 else f"{_fmt(abs_im)}i"
        if re_val == 0:
            return im_str if im_val > 0 else f"-{im_str}"
        sign = " + " if im_val > 0 else " - "
        return f"{re_str}{sign}{im_str}"

    # --- Parsing ---

    @staticmethod
    def parse(s: str) -> 'Gauss':
        """Parse from canonical 'A,B,C,D' format."""
        parts = s.strip().split(",")
        if len(parts) != 4:
            raise ValueError(f"Expected 'A,B,C,D' format, got: {s}")
        a, b, c, d = [int(x.strip()) for x in parts]
        return Gauss(Fraction(a, b), Fraction(c, d))

    @staticmethod
    def from_pramana(s: str) -> 'Gauss':
        """Parse from 'pra:num:A,B,C,D' format."""
        prefix = "pra:num:"
        if not s.startswith(prefix):
            raise ValueError(f"Expected format 'pra:num:A,B,C,D', got: {s}")
        return Gauss.parse(s[len(prefix):])

    # --- Static math methods ---

    @staticmethod
    def floor(value: 'Gauss') -> 'Gint':
        return Gint(math.floor(value.real), math.floor(value.imag))

    @staticmethod
    def ceil(value: 'Gauss') -> 'Gint':
        return Gint(math.ceil(value.real), math.ceil(value.imag))

    @staticmethod
    def truncate(value: 'Gauss') -> 'Gint':
        return Gint(math.trunc(value.real), math.trunc(value.imag))

    @staticmethod
    def min(*args):
        return builtins.min(args)

    @staticmethod
    def max(*args):
        return builtins.max(args)

    @staticmethod
    def clamp(value: 'Gauss', min_val: 'Gauss', max_val: 'Gauss') -> 'Gauss':
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value

    @staticmethod
    def sign(value: 'Gauss') -> int:
        """Return sign for real Gauss values: -1, 0, or 1."""
        if value.imag != Fraction(0):
            raise ValueError("sign is only defined for real values")
        if value.real > 0:
            return 1
        elif value.real < 0:
            return -1
        return 0

    @staticmethod
    def exact_abs(value: 'Gauss') -> 'Gauss':
        """Return exact absolute value for real Gauss values."""
        if value.imag != Fraction(0):
            raise ValueError("exact_abs is only defined for real values")
        if value.real < 0:
            return Gauss(-value.real)
        return Gauss(value.real)

    def __round__(self) -> 'Gint':
        return Gint(round(self.real), round(self.imag))

    def __floor__(self) -> 'Gint':
        return Gint(math.floor(self.real), math.floor(self.imag))

    def __ceil__(self) -> 'Gint':
        return Gint(math.ceil(self.real), math.ceil(self.imag))

    @property
    def conjugate(self):
        return Gauss(self.real, -self.imag)

    @property
    def norm(self) -> Fraction:
        tmp = self * self.conjugate
        return tmp.real

    @staticmethod
    def random(re1=-100, re2=100, im1=-100, im2=100):
        """Return a random Gaussian rational"""
        if re1 < re2 and im1 < im2 and re2 >= 1 and im2 >= 1:
            numerator = Gint.random(re1, re2, im1, im2)
            denominator = Gint.random(1, re2, 1, im2)
        else:
            raise ValueError(f"Bad range")
        return numerator / denominator

    @property
    def inverse(self):
        conj = self.conjugate
        norm = self.norm
        return Gauss(conj.real / norm, conj.imag / norm)

    @staticmethod
    def eye():
        """Return i = Gauss(0, 1)"""
        return Gauss(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Gauss values."""
        return [Gauss(1), -Gauss(1), Gauss.eye(), -Gauss.eye()]

    def associates(self):
        """Return a list of this Gauss's three associates"""
        us = Gauss.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Gauss is an associate of this Gauss, return False otherwise"""
        q = self / other
        if q:
            if q in Gint.units():
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def string_to_rational(qi_str):
        """Turn the string form of a Gaussian rational into a Gauss instance."""

        insides = qi_str[1:-2]  # Remove leading (and trailing j)

        # Separate leading sign, if it exists, from the main body of the string
        if insides[0] == '-' or insides[0] == '+':
            sign = insides[0]  # Leading sign
            body = insides[1:]
        else:
            sign = ''  # No leading sign
            body = insides

        # Split body of string into real & imag parts, based on imag sign
        if '+' in body:
            re, im = body.split('+')
            return Gauss(sign + re, im)
        elif '-' in body:
            re, im = body.split('-')
            return Gauss(sign + re, '-' + im)
        else:
            raise ValueError(f"Can't parse {qi_str}")


Gauss.ZERO = Gauss(0, 0)
Gauss.ONE = Gauss(1, 0)
Gauss.MINUS_ONE = Gauss(-1, 0)
Gauss.I = Gauss(0, 1)

# Backward-compatible aliases (original mathematical names from Dr. Reich's library)
Zi = Gint
"""Backward-compatible alias: Zi is the mathematical name for Gint (Z[i])."""

Qi = Gauss
"""Backward-compatible alias: Qi is the mathematical name for Gauss (Q[i])."""
