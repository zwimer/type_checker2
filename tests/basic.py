from types import NoneType
from pathlib import Path
import unittest

from simple_type_check import type_check


class TestBasic(unittest.TestCase):
    """
    Test type-checking for basic
    """

    def test_basic(self):
        self.assertTrue(type_check(1, int))
        self.assertTrue(type_check(1, int))
        self.assertTrue(type_check(True, bool))
        self.assertTrue(type_check(2.5, float))
        self.assertTrue(type_check("s", str))
        self.assertTrue(type_check(Path("/a"), Path))

    def test_none(self):
        self.assertTrue(type_check(NoneType, type))
        self.assertTrue(type_check(None, NoneType))
        self.assertTrue(type_check(None, None))

    def test_bool_is_int(self):
        type_check._bool_is_int = True
        self.assertTrue(type_check(True, int))
        type_check._bool_is_int = False
        self.assertFalse(type_check(True, int))

    def test_failures(self):
        self.assertFalse(type_check("1", int))
        self.assertFalse(type_check(True, str))
        self.assertFalse(type_check(2.5, None))
        self.assertFalse(type_check(None, int))


if __name__ == "__main__":
    unittest.main()
