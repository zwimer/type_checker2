from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Any
    from collections.abc import Callable


class Checker:
    def __init__(self, f: Callable[[Any, Any], bool]):
        self._check = f

    def __call__(self, obj: Any, type_: Any) -> bool:
        """
        :param: The object to check the type of
        :param: The type to required obj to be
        :raise: ValueError if type_ is invalid or cannot be reasonably checked
        """
        raise NotImplementedError()
