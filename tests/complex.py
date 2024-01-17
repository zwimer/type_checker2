from typing import ContextManager, Callable, Any
import unittest

from simple_type_check import type_check


class Base1:
    pass


class Derived1(Base1):
    pass


class CM:
    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass


class TestComplex(unittest.TestCase):
    """
    Test type checking for unions
    """

    def test_type(self):
        self.assertTrue(type_check(int, type))
        self.assertFalse(type_check(0, type))
        self.assertTrue(type_check(Base1, type[Base1]))
        self.assertTrue(type_check(Derived1, type[Base1]))
        self.assertFalse(type_check(CM, type[Base1]))
        self.assertFalse(type_check(Base1, type[Derived1]))
        self.assertTrue(type_check(Derived1, type[Derived1]))

    def test_context_manager(self):
        self.assertTrue(type_check(CM(), ContextManager))
        self.assertFalse(type_check(1, ContextManager))
        with self.assertRaises(ValueError):
            type_check(CM(), ContextManager[int])
        self.assertTrue(type_check(CM(), ContextManager[Any]))
        try:
            # Some versions of python are not ok with ... being the yield value
            self.assertTrue(type_check(CM(), ContextManager[...]))
        except TypeError:
            pass

    def test_callable(self):
        self.assertTrue(type_check(lambda: 1, Callable))
        self.assertTrue(type_check(type_check, Callable))
        self.assertTrue(type_check(self.test_callable, Callable))
        self.assertFalse(type_check(1, Callable))
        with self.assertRaises(ValueError):
            type_check(type_check, Callable[..., int])
        try:
            # Some versions of python are not ok with ... being a return value
            self.assertTrue(type_check(type_check, Callable[..., ...]))
        except TypeError:
            pass
        self.assertTrue(type_check(type_check, Callable[..., Any]))


if __name__ == "__main__":
    unittest.main()
