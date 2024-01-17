from __future__ import annotations
from typing import get_origin, get_args, cast
import collections
import contextlib
import typing
import types


from ..checker import Checker


if typing.TYPE_CHECKING:
    from typing import Any


__all__ = ("COMPLEX",)


class _BuiltinBasic(Checker):
    _TYPE: type | None = None

    def __call__(self, obj: Any, type_: Any) -> bool:
        """
        Raises ValueError if type_ is invalid
        """
        if self._TYPE is None:
            raise NotImplementedError()
        # pylint: disable=isinstance-second-argument-not-valid-type
        if self._TYPE not in (type_, get_origin(type_)) or not isinstance(obj, self._TYPE):
            return False
        args = get_args(type_)
        return self._check_args(obj, args) if args else True

    def _check_args(self, obj: Any, args: tuple) -> bool:
        raise NotImplementedError()


class Type(_BuiltinBasic):
    _TYPE = type

    def _check_args(self, obj: Any, args: tuple) -> bool:
        if len(args) != 1:
            raise ValueError(f"type object may only have 0 or 1 parameter. Not: {args}")
        return issubclass(obj, args[0])


class Dict(_BuiltinBasic):
    _TYPE = dict

    def _check_args(self, obj: Any, args: tuple) -> bool:
        if len(args) != 2:
            raise ValueError(f"dict object may only have 0 or 2 parameters. Not: {args}")
        for i in obj.items():
            if not self._check(i[0], args[0]):
                return False
            if len(args) == 2 and not self._check(i[1], args[1]):
                return False
        return True


class Tuple(_BuiltinBasic):
    _TYPE = tuple

    def _check_args(self, obj: Any, args: tuple) -> bool:
        if len(args) == 2 and args[1] == ...:  # ... is not a wild card in this instance
            return all(self._check(i, args[0]) for i in cast(tuple, obj))
        return len(args) == len(cast(tuple, obj)) and all(self._check(*x) for x in zip(cast(tuple, obj), args))


class _ListSetChecker(_BuiltinBasic):
    def _check_args(self, obj: Any, args: tuple) -> bool:
        if len(args) != 1:
            raise ValueError(f"Too many type arguments: {args}")
        arg = args[0]
        return all(self._check(i, arg) for i in typing.cast(list | set, obj))


class List(_ListSetChecker):
    _TYPE = list


class Set(_ListSetChecker):
    _TYPE = set


class AnyChecker(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        return type_ == typing.Any


class EllipsisChecker(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        return type_ == ...


class Union(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        ok = (types.UnionType, typing.Union)
        if type_ in ok:
            raise ValueError(f"Unions must have arguments: {type_}")
        if get_origin(type_) not in ok:
            return False
        return any(self._check(obj, i) for i in get_args(type_))


class ContextManager(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        if contextlib.AbstractContextManager not in (type_, get_origin(type_)):
            return False
        if (args := get_args(type_)) and (len(args) != 1 or args[0] not in (typing.Any, ...)):
            raise ValueError("Cannot check the return type of a context manager")
        return hasattr(obj, "__enter__") and hasattr(obj, "__exit__")


class Callable(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        ok = (types.FunctionType, collections.abc.Callable)
        if type_ not in ok and get_origin(type_) not in ok:
            return False
        if args := get_args(type_):
            if len(args) != 2:
                raise ValueError("Callable must have 0 or 2 arguments. Invalid: {type_}")
            if args[0] != ... or args[1] not in (typing.Any, ...):
                raise ValueError("Cannot check Callable arg / return types")
        return callable(obj)


COMPLEX: tuple[type[Checker], ...] = (
    Type,
    Tuple,
    List,
    Dict,
    Set,
    AnyChecker,
    EllipsisChecker,
    Union,
    ContextManager,
    Callable,
)
