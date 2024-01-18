import unittest

from simple_type_check import type_check, TypeCheckFailed


#
# Testable functions
#


@type_check.returns
def id_r(_: str) -> int:
    return _  # type: ignore


@type_check.args
def id_a(_: int) -> str:
    return _  # type: ignore


@type_check.decorate()
def big(a: int, /, b, c: float, *args: bytes, d: str, e: int | None = None, **kwargs: int) -> bool:
    return b


#
# Tests
#


@type_check.decorate()
def small(a: int, b: int) -> None:
    pass


class TestTypeCheck(unittest.TestCase):
    """
    Test type checking for unions
    """

    def test_args(self):
        _ = id_a(1)
        with self.assertRaises(TypeCheckFailed):
            _ = id_a("s")

    def test_returns(self):
        _ = id_r(1)
        with self.assertRaises(TypeCheckFailed):
            _ = id_r("s")

    def test_call(self):
        self.assertTrue(type_check(1, int))
        self.assertFalse(type_check(1, str))

    def test_require(self):
        type_check.require(1, int)
        with self.assertRaises(TypeCheckFailed):
            type_check.require(1, str)


class TestTypeCheckDecorator(unittest.TestCase):
    def test_illegal(self):
        small(1, 1)
        small(1, b=1)
        small(a=1, b=1)
        with self.assertRaises(TypeError):  # Out of order
            small(1, a=1)
        with self.assertRaises(TypeError):  # Too few
            small(1)
        with self.assertRaises(TypeError):  # Too many args
            small(1, 1, 1)
        with self.assertRaises(TypeError):  # dup
            small(1, 1, b=3)
        with self.assertRaises(TypeError):  # Too many kwargs
            small(1, 1, c=3)

    def test_basic(self):
        big(0, True, 1.0, d="")
        big(0, b=True, c=1.0, d="")
        big(0, True, 1.0, b"", d="", e=None, f=1)

    def test_return(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, 2, 1.0, d="")

    def test_arg_pos_only(self):
        with self.assertRaises(TypeCheckFailed):
            big(True, True, 1.0, d="")

    def test_arg_either(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, True, True, d="")
        with self.assertRaises(TypeCheckFailed):
            big(0, True, c=True, d="")

    def test_arg_var_pos(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, True, d="")
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, b"", True, d="")

    def test_arg_key_only(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, d=True)

    def test_arg_var_key(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, d="", f=False)
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, d="", f=1, g=False)

    def test_arg_default(self):
        with self.assertRaises(TypeCheckFailed):
            big(0, True, 1.0, d="", e=False)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            big(0, True, d="")
        with self.assertRaises(TypeError):
            big(0, True, 1.0)


if __name__ == "__main__":
    unittest.main()
