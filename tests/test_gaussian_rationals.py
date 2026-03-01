"""Tests for Gauss (Gaussian Rational) class.

Adapted from https://github.com/alreich/gaussian_integers
Original author: Alfred J. Reich, Ph.D. (MIT License)
Refactored: Qi -> Gauss, Zi -> Gint per Pramana naming conventions.
"""

from unittest import TestCase
from pramana import Gint, Gauss
from fractions import Fraction
from random import seed


class TestGauss(TestCase):

    def setUp(self) -> None:
        self.q1 = Gauss(2, 3.4)

        self.f1 = Fraction(1, 2)
        self.f2 = Fraction(3, 5)
        self.q2 = Gauss(self.f1, self.f2)

        self.q3 = Gauss("4/6", "-1/7")

        self.c1 = (2.2 - 7.4j)
        self.q4 = Gauss(self.c1)

        self.z1 = Gint(-2, 3)
        self.q5 = Gauss(self.z1)

    def testConstructor(self):
        self.assertEqual(self.q1, Gauss(2, '17/5'))
        self.assertEqual(self.q2, Gauss('1/2', '3/5'))
        self.assertEqual(self.q3, Gauss('2/3', '-1/7'))  # 4/6 --> 2/3
        self.assertEqual(self.q4, Gauss('11/5', '-37/5'))
        self.assertEqual(self.q5, Gauss(-2, 3))

    def test_max_denominator(self):
        self.assertEqual(Gauss.max_denominator(), 1000000)

    def test_real(self):
        self.assertEqual(self.q1.real, Fraction(2, 1))

    def test_imag(self):
        self.assertEqual(self.q1.imag, Fraction(17, 5))

    def test_conjugate(self):
        self.assertEqual(self.q1.conjugate, Gauss(2, '-17/5'))

    def test_repr(self):
        self.assertEqual(repr(self.q1), "Gauss('2', '17/5')")

    def test_str(self):
        self.assertEqual(str(self.q1), '(2+17/5j)')
        self.assertEqual(str(self.q2), '(1/2+3/5j)')
        self.assertEqual(str(self.q3), '(2/3-1/7j)')

    def test_string_to_rational(self):
        self.assertEqual(Gauss.string_to_rational('(1/2+3/5j)'), Gauss('1/2', '3/5'))
        self.assertEqual(Gauss.string_to_rational('(1/2-3/5j)'), Gauss('1/2', '-3/5'))
        self.assertEqual(Gauss.string_to_rational('(-1/2+3/5j)'), Gauss('-1/2', '3/5'))
        self.assertEqual(Gauss.string_to_rational('(-1/2-3/5j)'), Gauss('-1/2', '-3/5'))
        self.assertEqual(Gauss.string_to_rational('(+1/2+3/5j)'), Gauss('1/2', '3/5'))
        self.assertEqual(Gauss.string_to_rational('(+1/2-3/5j)'), Gauss('1/2', '-3/5'))

        self.assertEqual(Gauss.string_to_rational('(1/2+3j)'), Gauss('1/2', 3))
        self.assertEqual(Gauss.string_to_rational('(1-3/5j)'), Gauss(1, '-3/5'))
        self.assertEqual(Gauss.string_to_rational('(+1-3/5j)'), Gauss(1, '-3/5'))
        self.assertEqual(Gauss.string_to_rational('(-2+5j)'), Gauss(-2, 5))
        self.assertEqual(Gauss.string_to_rational('(-1-3j)'), Gauss(-1, -3))
        self.assertEqual(Gauss.string_to_rational('(+2+5j)'), Gauss(2, 5))
        self.assertEqual(Gauss.string_to_rational('(+1-3j)'), Gauss(1, -3))

    def test_addition(self):
        self.assertEqual(self.q1 + self.q2, Gauss('5/2', 4))

        self.assertEqual(self.q1 + 1, Gauss(3, '17/5'))
        self.assertEqual(self.q1 + 1, Gauss(3, '17/5'))

        self.assertEqual(self.q1 + 1.5, Gauss('7/2', '17/5'))
        self.assertEqual(1.5 + self.q1, Gauss('7/2', '17/5'))

        self.assertEqual(self.q1 + (1.5 + 2j), Gauss('7/2', '27/5'))
        self.assertEqual((1.5 + 2j) + self.q1, Gauss('7/2', '27/5'))

    def test_subtraction(self):
        self.assertEqual(self.q1 - self.q2, Gauss('3/2', '14/5'))

        self.assertEqual(self.q1 - 1, Gauss(1, '17/5'))
        self.assertEqual(1 - self.q1, Gauss(-1, '-17/5'))

        self.assertEqual(self.q1 - 1.5, Gauss('1/2', '17/5'))
        self.assertEqual(1.5 - self.q1, Gauss('-1/2', '-17/5'))

        self.assertEqual(self.q1 - (1.5 + 2j), Gauss('1/2', '7/5'))
        self.assertEqual((1.5 + 2j) - self.q1, Gauss('-1/2', '-7/5'))

    def test_multiplication(self):
        self.assertEqual(self.q1 * self.q2, Gauss('-26/25', '29/10'))

        self.assertEqual(self.q1 * 2, Gauss(4, '34/5'))
        self.assertEqual(2 * self.q1, Gauss(4, '34/5'))

        self.assertEqual(self.q1 * 2.2, Gauss('22/5', '187/25'))
        self.assertEqual(2.2 * self.q1, Gauss('22/5', '187/25'))

        self.assertEqual(self.q1 * (2.2 - 3.6j), Gauss('416/25', '7/25'))
        self.assertEqual((2.2 - 3.6j) * self.q1, Gauss('416/25', '7/25'))

    def test_inverse(self):
        self.assertEqual(self.q1.inverse, Gauss('50/389', '-85/389'))

    def test_division(self):
        a = self.q1
        self.assertEqual(a / self.q2, Gauss('304/61', '50/61'))
        self.assertEqual(a / 2, Gauss('1', '17/10'))
        self.assertEqual(2 / a, Gauss('100/389', '-170/389'))
        self.assertEqual(a / 2.4, Gauss('5/6', '17/12'))
        self.assertEqual(2.4 / a, Gauss('120/389', '-204/389'))
        self.assertEqual(a / Gint(7, -6), Gauss('-32/425', '179/425'))
        self.assertEqual(Gint(7, -6) / a, Gauss('-160/389', '-895/389'))
        self.assertEqual(Gint(2, 6) / Gint(4, 5), Gauss('38/41', '14/41'))

    def test_power(self):
        self.assertEqual(self.q1 ** 3, Gauss('-1534/25', '187/125'))

    def test_norm(self):
        self.assertEqual(self.q1.norm, Fraction(389, 25))

    def test_negation(self):
        self.assertEqual(-self.q2, Gauss('-1/2', '-3/5'))

    def test_equality(self):
        self.assertTrue(self.q1 == Gauss(2, '17/5'))
        self.assertTrue(Gauss(2, 0) == 2)
        self.assertTrue(Gauss(2, 0) == 2.0)
        self.assertTrue(Gauss(2, 0) == (2+0j))
        self.assertTrue(Gauss('1/2', 0) == Fraction(1, 2))

    def test_inequality(self):
        self.assertTrue(self.q1 != self.q2)
        self.assertTrue(Gauss(2, 0) != 3)
        self.assertTrue(Gauss(2, 0) != 3.0)
        self.assertTrue(Gauss(2, 0) != (3-2j))
        self.assertTrue(Gauss('1/2', 0) != Fraction(2, 3))

    def test_eye(self):
        self.assertEqual(Gauss.eye(), Gauss(0, 1))

    def test_units(self):
        self.assertEqual(Gauss.units(), [Gauss('1', '0'), Gauss('-1', '0'), Gauss('0', '1'), Gauss('0', '-1')])

    def test_associates(self):
        self.assertEqual(self.q2.associates(), [Gauss('-1/2', '-3/5'), Gauss('-3/5', '1/2'), Gauss('3/5', '-1/2')])

    def test_is_associate(self):
        self.assertTrue(self.q2.is_associate(Gauss('-1/2', '-3/5')))
        self.assertFalse(self.q2.is_associate(self.q1))

    def test_random(self):
        seed(7)
        self.assertEqual(Gauss.random(), Gauss('-2042/3219', '-550/3219'))

    def test_backward_compat_alias(self):
        """Verify that Qi is an alias for Gauss."""
        from pramana import Qi
        self.assertIs(Qi, Gauss)
        self.assertEqual(Qi('1/2', '3/5'), Gauss('1/2', '3/5'))
