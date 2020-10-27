
from unittest import TestCase

from pymapadmin import is_compatible


class TestVersion(TestCase):

    def test_is_compatible(self) -> None:
        self.assertTrue(is_compatible('1.0', '1.0'))
        self.assertTrue(is_compatible('1.0', '1.1'))
        self.assertTrue(is_compatible('1.0', '1.10'))
        self.assertFalse(is_compatible('1.0', '2.0'))
        self.assertFalse(is_compatible('1.0', '2.1'))
        self.assertFalse(is_compatible('1.0', '2.10'))
        self.assertTrue(is_compatible('0.1.0', '0.1.0'))
        self.assertTrue(is_compatible('0.1.0', '0.1.1'))
        self.assertTrue(is_compatible('0.1.0', '0.1.10'))
        self.assertFalse(is_compatible('0.1.0', '0.2.0'))
        self.assertFalse(is_compatible('0.1.0', '0.2.1'))
        self.assertFalse(is_compatible('0.1.0', '0.2.10'))
