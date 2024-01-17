import unittest
import typing

from simple_type_check import type_check


class TestListSet(unittest.TestCase):
    """
    Test type-checking for lists and sets
    """

    _TYPES = {set: set, typing.Set: set, list: list, typing.List: list}

    def test_each(self):
        for typ, ctor in self._TYPES.items():
            self.assertTrue(type_check(ctor(), typ))
            self.assertFalse(type_check(0, typ))

    def test_0_arg(self):
        for typ, ctor in self._TYPES.items():
            self.assertTrue(type_check(ctor(), typ))
            self.assertTrue(type_check(ctor([0]), typ))
            self.assertTrue(type_check(ctor([0, "s"]), typ))

    def test_1_arg(self):
        for typ, ctor in self._TYPES.items():
            self.assertTrue(type_check(ctor(), typ[int]))
            self.assertTrue(type_check(ctor([0]), typ[int]))
            self.assertFalse(type_check(ctor([0]), typ[str]))
            self.assertTrue(type_check(ctor([0, 1]), typ[int]))
            self.assertFalse(type_check(ctor([0, "s"]), typ[int]))

    def test_illegal(self):
        for typ, ctor in self._TYPES.items():
            try:  # Only test these if python doesn't fail you for even trying
                illegal1 = typ[str, int]
            except TypeError:
                continue
            with self.assertRaises(ValueError):
                type_check(ctor([1]), illegal1)


if __name__ == "__main__":
    unittest.main()
