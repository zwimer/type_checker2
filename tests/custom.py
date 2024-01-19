import unittest
import typing

from simple_type_check import TypeChecker
from simple_type_check.top_level_check import TopLevelCheck


class Basic1:
    pass


class Other1:
    pass


class Complex1:
    def __init__(self, b: bool):
        self.valid: bool = b


class Complex1Check(TopLevelCheck):
    def __call__(self, obj: typing.Any, type_: typing.Any) -> bool:
        return type_ == Complex1 and isinstance(obj, Complex1) and obj.valid


type_check = TypeChecker(Basic1, advanced=(Complex1Check,))


class TestCustom(unittest.TestCase):
    """
    Test type checking for custom types
    """

    _TYPES = (int | None, typing.Union[int, None], typing.Optional[int])

    def test_basic(self):
        b = Basic1()
        self.assertTrue(type_check(b, Basic1))
        self.assertFalse(type_check(b, Other1))
        self.assertFalse(type_check(b, Complex1))
        self.assertFalse(type_check(b, int))
        self.assertTrue(type_check(b, typing.Any))

    def test_other(self):
        o = Other1()  # Not registered, so cannot check
        self.assertFalse(type_check(o, Basic1))
        self.assertFalse(type_check(o, Other1))
        self.assertFalse(type_check(o, Complex1))
        self.assertTrue(type_check(o, typing.Any))  # AnyChecker can check

    def test_complex(self):
        c = Complex1(False)
        self.assertFalse(type_check(c, Basic1))
        self.assertFalse(type_check(c, Other1))
        self.assertFalse(type_check(c, Complex1))
        self.assertTrue(type_check(c, typing.Any))  # AnyChecker can check
        c.valid = True
        self.assertTrue(type_check(c, Complex1))


if __name__ == "__main__":
    unittest.main()
