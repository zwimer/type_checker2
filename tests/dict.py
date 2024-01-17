import unittest
import typing

from simple_type_check import type_check


class TestDict(unittest.TestCase):
    """
    Test type checking dicts
    """

    _DICTS = (dict, typing.Dict)

    def test_each(self):
        for dct in self._DICTS:
            self.assertTrue(type_check({}, dct))
            self.assertFalse(type_check([], dct))

    def test_0_arg(self):
        for dct in self._DICTS:
            self.assertTrue(type_check({1: 1}, dct))
            self.assertTrue(type_check({"s": True}, dct))
            self.assertTrue(type_check({1: 1, "s": bool}, dct))

    def test_2_arg(self):
        for dct in self._DICTS:
            self.assertTrue(type_check({}, dct[str, int]))
            self.assertTrue(type_check({"1": 1}, dct[str, int]))
            self.assertFalse(type_check({1: 1}, dct[str, int]))
            self.assertTrue(type_check({b"": "s", b"1": "3"}, dct[bytes, str]))
            self.assertFalse(type_check({b"": "s", b"1": 3}, dct[bytes, str]))

    def test_illegal(self):
        for dct in self._DICTS:
            try:  # Only test these if python doesn't fail you for even trying
                illegal1 = dct[str]
                illegal2 = dct[str]
            except TypeError:
                continue
            with self.assertRaises(ValueError):
                type_check({}, illegal1)
            with self.assertRaises(ValueError):
                type_check({"1": 1}, illegal2)

    def test_extras(self):
        for dct in (dict, typing.Dict):
            self.assertTrue(type_check({"1": {}}, dct))
            self.assertTrue(type_check({"1": {}}, dct[str, dct]))
            self.assertTrue(type_check({"1": {}}, dct[str, dct[str, int]]))
            self.assertTrue(type_check({"1": {"2": 3}}, dct[str, dct[str, int]]))
            self.assertFalse(type_check({"1": {"2": 3}}, dct[str, dct[str, str]]))
            self.assertTrue(type_check({"1": {"2": 3}, "4": {"5": "6"}}, dct[str, dct]))
            self.assertFalse(type_check({"1": {"2": 3}, "4": {"5": "6"}}, dct[str, dct[str, int]]))


if __name__ == "__main__":
    unittest.main()
