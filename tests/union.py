import unittest
import typing

from simple_type_check import type_check


class TestUnion(unittest.TestCase):
    """
    Test type checking for unions
    """

    _TYPES = (int | None, typing.Union[int, None], typing.Optional[int])

    def test_any(self):
        self.assertTrue(type_check(None, typing.Any))
        self.assertTrue(type_check(type, typing.Any))
        self.assertTrue(type_check([], typing.Any))
        self.assertTrue(type_check(1, typing.Any))

    def test_each(self):
        for i in self._TYPES:
            self.assertTrue(type_check(None, i))
            self.assertTrue(type_check(1, i))
            self.assertFalse(type_check("1", i))


if __name__ == "__main__":
    unittest.main()
