"""Tests for Gint (Gaussian Integer) class.

Adapted from https://github.com/alreich/gaussian_integers
Original author: Alfred J. Reich, Ph.D. (MIT License)
Refactored: Zi -> Gint, Qi -> Gauss per Pramana naming conventions.
"""

from unittest import TestCase
from pramana import Gint, Gauss


class TestGint(TestCase):

    def setUp(self) -> None:
        self.c1 = Gint(4, 5)
        self.c1_conj = Gint(4, -5)
        self.c2 = Gint(1, -2)
        self.c1_x_c2 = Gint(14, -3)  # c1 * c2
        self.c4 = Gint(4, 12)

    def test_constructor(self):
        self.assertEqual(Gint(), Gint(0, 0))
        self.assertEqual(Gint(1), Gint(1, 0))
        self.assertEqual(Gint.eye(), Gint(0, 1))
        self.assertEqual(Gint.two(), Gint(1, 1))
        self.assertEqual(Gint(2.3, 3.8), Gint(2, 4))
        self.assertEqual(Gint(-2.3, 3.8), Gint(-2, 4))
        self.assertEqual(Gint(2.3, -3.8), Gint(2, -4))
        self.assertEqual(Gint(-2.3, -3.8), Gint(-2, -4))
        self.assertEqual(Gint(2.3, 4), Gint(2, 4))
        self.assertEqual(Gint(-2.3, 4), Gint(-2, 4))
        self.assertEqual(Gint(2, 3.8), Gint(2, 4))
        self.assertEqual(Gint(2, -3.8), Gint(2, -4))
        self.assertEqual(Gint(2.3), Gint(2, 0))
        self.assertEqual(Gint(2), Gint(2, 0))
        self.assertEqual(Gint((2.3 - 3.7j)), Gint(2, -4))
        self.assertEqual(Gint(-3.3j), Gint(0, -3))

    def test_repr(self):
        self.assertEqual(repr(self.c1), "Gint(4, 5)")
        self.assertEqual(repr(Gint(3)), "Gint(3)")

    def test_add(self):
        self.assertEqual(Gint(4, 5) + Gint(1, -2), Gint(5, 3))
        self.assertEqual(Gint(4, 5) + 2, Gint(6, 5))
        self.assertEqual(2 + Gint(4, 5), Gint(6, 5))
        self.assertEqual(Gint(4, 5) + 1.9, Gint(6, 5))
        self.assertEqual(1.9 + Gint(4, 5), Gint(6, 5))
        self.assertEqual(Gint(4, 5) + (1-1j), Gint(5, 4))
        self.assertEqual((1 - 1j) + Gint(4, 5), Gint(5, 4))

    def test_sub(self):
        self.assertEqual(Gint(4, 5) - Gint(1, -2), Gint(3, 7))
        self.assertEqual(Gint(4, 5) - 2, Gint(2, 5))
        self.assertEqual(2 - Gint(4, 5), Gint(-2, -5))
        self.assertEqual(Gint(4, 5) - 1.9, Gint(2, 5))
        self.assertEqual(1.9 - Gint(4, 5), Gint(-2, -5))
        self.assertEqual(Gint(4, 5) - (1 - 1j), Gint(3, 6))
        self.assertEqual((1 - 1j) - Gint(4, 5), Gint(-3, -6))

    def test_mul(self):
        self.assertEqual(Gint(4, 5) * Gint(1, -2), Gint(14, -3))
        self.assertEqual(Gint(4, 5) * 2, Gint(8, 10))
        self.assertEqual(2 * Gint(4, 5), Gint(8, 10))
        self.assertEqual(Gint(4, 5) * 1.9, Gint(8, 10))
        self.assertEqual(1.9 * Gint(4, 5), Gint(8, 10))
        self.assertEqual(Gint(4, 5) * 1.49999, Gint(4, 5))
        self.assertEqual(1.49999 * Gint(4, 5), Gint(4, 5))
        self.assertEqual(Gint(4, 5) * (2-1j), Gint(13, 6))
        self.assertEqual((2-1j) * Gint(4, 5), Gint(13, 6))
        self.assertEqual(Gint(4, 5) * (1.9-1.1j), Gint(13, 6))
        self.assertEqual((1.9-1.1j) * Gint(4, 5), Gint(13, 6))

    def test_truediv(self):
        self.assertEqual(Gint(4, 5) / Gint(1, -2), Gauss('-6/5', '13/5'))
        self.assertEqual(Gint(4, 5) / (1.1 - 1.9j), Gauss('-255/241', '655/241'))
        self.assertEqual(Gint(4, 5) / (0.9 - 2.3j), Gauss('-79/61', '137/61'))
        self.assertEqual(complex(Gint(4, 5) / (0.9 - 2.3j)), (-1.2950819672131149 + 2.2459016393442623j))
        self.assertEqual(complex(Gint(4, 5)) / (0.9 - 2.3j), (-1.2950819672131149 + 2.2459016393442623j))
        self.assertEqual(Gint(4, 5) / 5, Gauss('4/5', '1'))
        self.assertEqual(Gint(4, 8) / 2, Gint(2, 4))
        self.assertEqual(Gint(4, 5) / 5.3, Gauss('40/53', '50/53'))
        self.assertEqual((1 - 2j) / Gint(4, 5), Gauss('-6/41', '-13/41'))
        self.assertEqual(5.0 / Gint(4, 5), Gauss('20/41', '-25/41'))
        self.assertEqual(5 / Gint(4, 5), Gauss('20/41', '-25/41'))

    def test_neg(self):
        self.assertEqual(-Gint(1, -2), Gint(-1, 2))

    def test_pow(self):
        self.assertEqual(self.c1 ** 3, Gint(-236, 115))
        self.assertEqual(self.c1 ** 1, self.c1)
        self.assertEqual(self.c1 ** 0, Gint(1))

    def test_complex(self):
        self.assertEqual(complex(self.c1), (4+5j))

    def test_str(self):
        self.assertEqual(str(self.c1), "4 + 5i")

    def test_equal(self):
        self.assertTrue(self.c1 == Gint(4, 5))
        self.assertFalse(self.c1 == self.c2)

    def test_not_equal(self):
        self.assertTrue(self.c1 != self.c2)

    def test_eye(self):
        self.assertEqual(Gint.eye(), Gint(0, 1))

    def test_units(self):
        self.assertEqual(Gint.units(), [Gint(1, 0), Gint(-1, 0), Gint(0, 1), Gint(0, -1)])

    def test_conj(self):
        self.assertEqual(self.c1.conjugate, self.c1_conj)

    def test_norm(self):
        self.assertEqual(self.c1.norm, 41)

    def test_associates(self):
        self.assertEqual(self.c1.associates(), [Gint(-4, -5), Gint(-5, 4), Gint(5, -4)])

    def test_is_associate(self):
        self.assertTrue(self.c1.is_associate(Gint(-4, -5)))
        self.assertFalse(self.c1.is_associate(self.c2))

    def test_divmod_1(self):
        a = Gint(4, 5)
        b = Gint(1, -2)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_2(self):
        a = Gint(27, -23)
        b = Gint(8, 1)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_3(self):
        a = Gint(11, 10)
        b = Gint(4, 1)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_4(self):
        a = Gint(41, 24)
        b = Gint(11, -2)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_5(self):
        a = Gint(37, 2)
        b = Gint(11, 2)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_divmod_6(self):
        a = Gint(1, 8)
        b = Gint(2, -4)
        q, r = Gint.modified_divmod(a, b)
        self.assertEqual(a, b * q + r)

    def test_mod_1(self):
        a = Gint(4, 5)
        b = Gint(1, -2)
        self.assertEqual(a % b, -1)

    def test_gcd_1(self):
        alpha = Gint(32, 9)
        beta = Gint(4, 11)
        self.assertEqual(Gint.gcd(alpha, beta), Gint(0, -1))

    def test_gcd_2(self):
        alpha = Gint(32, 9)
        beta = Gint(4, 11)
        self.assertEqual(Gint.gcd(beta, alpha), Gint(0, -1))

    def test_gcd_3(self):
        alpha = Gint(11, 3)
        beta = Gint(1, 8)
        self.assertEqual(Gint.gcd(alpha, beta), Gint(1, -2))

    def test_backward_compat_alias(self):
        """Verify that Zi is an alias for Gint."""
        from pramana import Zi
        self.assertIs(Zi, Gint)
        self.assertEqual(Zi(4, 5), Gint(4, 5))

    # --- New v0.2.0 tests ---

    def test_str_formatting(self):
        self.assertEqual(str(Gint(3, 2)), "3 + 2i")
        self.assertEqual(str(Gint(3, -2)), "3 - 2i")
        self.assertEqual(str(Gint(3, 1)), "3 + i")
        self.assertEqual(str(Gint(3, -1)), "3 - i")
        self.assertEqual(str(Gint(0, 1)), "i")
        self.assertEqual(str(Gint(0, -1)), "-i")
        self.assertEqual(str(Gint(5, 0)), "5")
        self.assertEqual(str(Gint(0, 0)), "0")
        self.assertEqual(str(Gint(0, 3)), "3i")
        self.assertEqual(str(Gint(0, -3)), "-3i")

    def test_classification_properties(self):
        self.assertTrue(Gint(5).is_real)
        self.assertFalse(Gint(5, 3).is_real)
        self.assertTrue(Gint(0, 3).is_purely_imaginary)
        self.assertFalse(Gint(1, 3).is_purely_imaginary)
        self.assertFalse(Gint(0, 0).is_purely_imaginary)
        self.assertTrue(Gint(0, 0).is_zero)
        self.assertFalse(Gint(1).is_zero)
        self.assertTrue(Gint(5).is_integer)
        self.assertFalse(Gint(5, 3).is_integer)
        self.assertTrue(Gint(5, 3).is_gaussian_integer)
        self.assertTrue(Gint(1).is_one)
        self.assertFalse(Gint(2).is_one)
        self.assertTrue(Gint(5).is_positive)
        self.assertFalse(Gint(-5).is_positive)
        self.assertFalse(Gint(0, 3).is_positive)
        self.assertTrue(Gint(-5).is_negative)
        self.assertFalse(Gint(5).is_negative)

    def test_comparison_operators(self):
        self.assertTrue(Gint(1, 0) < Gint(2, 0))
        self.assertTrue(Gint(1, 2) < Gint(1, 3))
        self.assertFalse(Gint(2, 0) < Gint(1, 0))
        self.assertTrue(Gint(2, 0) > Gint(1, 0))
        self.assertTrue(Gint(1, 0) <= Gint(1, 0))
        self.assertTrue(Gint(1, 0) >= Gint(1, 0))
        self.assertTrue(Gint(1, 0) <= Gint(2, 0))
        self.assertTrue(Gint(2, 0) >= Gint(1, 0))

    def test_pramana_identity(self):
        g = Gint(3, 4)
        self.assertEqual(g.pramana_key, "3,1,4,1")
        self.assertTrue(g.pramana_id)  # UUID is non-empty
        self.assertTrue(g.pramana_url.startswith("https://pramana.dev/entity/"))
        self.assertEqual(g.pramana_label, "pra:num:3,1,4,1")
        # Verify deterministic: same input = same id
        g2 = Gint(3, 4)
        self.assertEqual(g.pramana_id, g2.pramana_id)
        # Different values give different ids
        g3 = Gint(3, 5)
        self.assertNotEqual(g.pramana_id, g3.pramana_id)

    def test_static_constants(self):
        self.assertEqual(Gint.ZERO, Gint(0, 0))
        self.assertEqual(Gint.ONE, Gint(1, 0))
        self.assertEqual(Gint.MINUS_ONE, Gint(-1, 0))
        self.assertEqual(Gint.I, Gint(0, 1))
