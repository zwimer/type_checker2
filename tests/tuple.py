import unittest
import typing

from simple_type_check import type_check


class TestTuple(unittest.TestCase):
    """
    Test type-checking for tuples
    """

    _TYPES = (tuple, typing.Tuple)

    def test_0_arg(self):
        for tup in self._TYPES:
            self.assertTrue(type_check(tuple(), tup))
            self.assertTrue(type_check((1,), tup))
            self.assertFalse(type_check([1], tup))
            self.assertFalse(type_check(1, tup))

    def test_1_arg(self):
        for tup in self._TYPES:
            self.assertTrue(type_check((1,), tup[int]))
            self.assertFalse(type_check((1,), tup[str]))
            self.assertFalse(type_check((1, 1), tup[int]))

    def test_ellipsis(self):
        for tup in self._TYPES:
            # Pass
            self.assertTrue(type_check((1,), tup[int, ...]))
            self.assertTrue(type_check((1, 2, 3), tup[int, ...]))
            # # Fail
            self.assertFalse(type_check(("",), tup[int, ...]))
            self.assertFalse(type_check((1, ""), tup[int, ...]))

    def test_multiple_arg(self):
        for tup in self._TYPES:
            self.assertTrue(type_check((1, True), tup[int, bool]))
            self.assertTrue(type_check((1, True, ""), tup[int, bool, str]))


if __name__ == "__main__":
    unittest.main()
