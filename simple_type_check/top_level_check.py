from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


class TopLevelCheck:
    """
    A class to be subclassed, determines if it can type check a given type annotation,and if so checks to
    see if an object is of said type. For example, a class DictCheck(TopLevelCheck)'s __call__ function
    would  return True given obj={1:2} type_=dict[int, int] as DictCheck can check things if objects
    are of type type_ or not.
    """

    def __init__(self, recurse: Callable[[Any, Any], bool]):
        """
        :param recurse: The type checker callable used to recurse if needed
        """
        self._recurse = recurse

    def __call__(self, obj: Any, type_: Any) -> bool:
        """
        :param: The object to check the type of
        :param: The type to required obj to be
        :raise: ValueError if type_ is invalid or cannot be reasonably checked
        """
        raise NotImplementedError()
