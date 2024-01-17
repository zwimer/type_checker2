import unittest

from simple_type_check import type_check, TypeCheckFailed


@type_check.returns(int)
def id(x):
    return x


class TestTypeCheck(unittest.TestCase):
    """
    Test type checking for unions
    """

    def test_returns(self):
        _ = id(1)
        with self.assertRaises(TypeCheckFailed):
            _ = id("s")

    def test_call(self):
        self.assertTrue(type_check(1, int))
        self.assertFalse(type_check(1, str))


if __name__ == "__main__":
    unittest.main()
