from __future__ import annotations
from typing import TYPE_CHECKING

from .default import COMPLEX, BASIC

if TYPE_CHECKING:
    from typing import Callable, Sequence, Any
    from .checker import Checker


class TypeCheckFailed(RuntimeError):
    """
    Raised when a decrator's type check fails
    """


class _NA:
    pass


_na = _NA()


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

    def returns(self, type_: Any) -> Callable:
        """
        A decorator that type checks a return type
        """

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                ret = func(*args, **kwargs)
                if not self(ret, type_):
                    raise TypeCheckFailed(f"Return type should be of type {type_}", ret)
                return ret

            return wrapper

        return decorator


type_check = TypeChecker()
