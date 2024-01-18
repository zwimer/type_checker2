from __future__ import annotations
from inspect import Parameter, signature
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping, Callable


_empty = Parameter.empty


@dataclass(kw_only=True, frozen=True)
class CallableInfo:
    name: str
    return_type: Parameter
    params: Mapping[str, Parameter]
    all_pos: tuple[Parameter, ...]
    all_key: tuple[str, ...]
    kwargs_param: Parameter | None
    args_param: Parameter | None
    needs_kw: tuple[Parameter, ...]

    @staticmethod
    def _get_vars(params: Mapping[str, Parameter], pos: bool) -> Parameter | None:
        ret = [i for i in params.values() if i.kind == (Parameter.VAR_POSITIONAL if pos else Parameter.VAR_KEYWORD)]
        assert len(ret) <= 1
        return ret[0] if ret else None

    @classmethod
    def new(cls, func: Callable) -> CallableInfo:
        s = signature(func)
        p: Mapping[str, Parameter] = s.parameters
        pos_kind = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
        key_kind = (Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
        kw_p = cls._get_vars(p, False)
        a_p = cls._get_vars(p, True)
        return cls(
            name=func.__name__,
            return_type=s.return_annotation,
            params=p,
            all_pos=tuple(k for k in p.values() if k.kind in pos_kind),
            all_key=tuple(i for i, k in p.items() if k.kind in key_kind),
            kwargs_param=kw_p,
            args_param=a_p,
            needs_kw=tuple(i for i in p.values() if i.default == Parameter.empty and i not in (kw_p, a_p)),
        )
