from __future__ import annotations
from typing import TYPE_CHECKING
from inspect import Parameter

from .default import COMPLEX, BASIC
from .callable_info import CallableInfo

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any
    from .checker import Checker


__all__ = ("TypeChecker", "TypeCheckFailed", "type_check")


class TypeCheckFailed(RuntimeError):
    """
    Raised when a decorator's type check fails
    """


class TypeChecker:
    def __init__(self, *basic: type, advanced: Sequence[type[Checker]] | None = None, bool_is_int: bool = False):
        """
        Construct a type-checker
        :param basic: Additional basic types to handle, where isinstance is sufficient for type checking
        :param advanced: Additional basic types to handle that are not in basic
        :param bool_is_int: If False, will treat bool and int as unrelated types; else booleans are integers
        """
        adv: tuple[type[Checker], ...] = COMPLEX + (tuple(advanced) if advanced else ())
        self._advanced: tuple[Checker, ...] = tuple(K(self) for K in adv)
        self._basic: tuple[type, ...] = tuple(BASIC | (set(basic) if basic else set()))
        self._bool_is_int: bool = bool_is_int

    def __call__(self, obj: Any, type_: Any) -> bool:
        """
        :param obj: Object to check the type of
        :param type_: Type to check
        :return: True if obj is of type type_, False otherwise
        """
        if obj is None and type_ is None:  # Special case for 'None' since 'None' isn't a type
            return True
        if type_ in self._basic:
            return isinstance(obj, type_) and (type_ != int or not isinstance(obj, bool) or self._bool_is_int)
        return any(k(obj, type_) for k in self._advanced)

    def require(self, obj: Any, type_: Any) -> None:
        """
        :param obj: Object to check the type of
        :param type_: Type to check
        :raises TypeCheckFailed: If obj is not of type_
        """
        if not self(obj, type_):
            raise TypeCheckFailed(obj, type_)

    def args(self, func: Callable) -> Callable:
        """
        A decorator that type checks argument types
        """
        return self.decorate(check_args=True, check_return=False)(func)

    def returns(self, func: Callable) -> Callable:
        """
        A decorator that type checks a return type
        """
        return self.decorate(check_args=False, check_return=True)(func)

    def _check_args(self, ci: CallableInfo, f_args: tuple[Any], f_kwargs: dict[str, Any]):
        # Find f_args and kwargs
        known: dict[Parameter, Any] = dict(zip(ci.all_pos, f_args))
        add_known = {ci.params[i]: k for i, k in f_kwargs.items() if i in ci.all_key}
        if dupes := tuple(i.name for i in known if i in add_known):
            raise TypeError(f"Duplicate arguments passed for: {', '.join(dupes)}")
        known |= add_known
        # Check for missing
        if missing := tuple(i.name for i in ci.needs_kw if i not in known):
            raise TypeError(f"{ci.name}() was not passed arguments: {', '.join(missing)}")
        # *args and **kwargs
        to_check: list[tuple[str | None, Any, Any]] = [(i.name, i, k) for i, k in known.items()]
        if args_vals := f_args[len(ci.all_pos) :]:
            if ci.args_param is None:
                raise TypeError(f"{ci.name}() passed {len(args_vals)} extra positional argument(s).")
            to_check += [(None, ci.args_param, i) for i in args_vals]
        known_names = {j.name for j in known}
        if kwargs_dict := {i: k for i, k in f_kwargs.items() if i not in known_names}:
            if ci.kwargs_param is None:
                raise TypeError(f"{ci.name}() passed extra keyword argument(s): {', '.join(kwargs_dict.keys())}")
            to_check += [(i, ci.kwargs_param, k) for i, k in kwargs_dict.items()]
        # Check types
        for name, param, obj in to_check:
            if (type_ := param.annotation) != Parameter.empty and not self(obj, type_):
                raise TypeCheckFailed(f"{ci.name}()'s argument {name} was not of type: {type_}")

    def decorate(self, check_args: bool = True, check_return: bool = True) -> Callable:
        def decorator(func: Callable) -> Callable:
            ci = CallableInfo.new(func)

            def wrapper(*f_args, **f_kwargs) -> Any:
                if check_args:
                    self._check_args(ci, f_args, f_kwargs)
                ret = func(*f_args, **f_kwargs)
                if check_return and ci.return_type != Parameter.empty and not self(ret, ci.return_type):
                    raise TypeCheckFailed(f"{func.__name__}()'s return type: {ci.return_type}")
                return ret

            return wrapper

        return decorator


type_check = TypeChecker()
