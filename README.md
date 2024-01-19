# simple\_type\_checker

A small extendable python type checker library

### Basic Usage

Checking a type:
```python
from simple_type_check import type_check
assert type_check("A string", str)
```

As a decorator:
```python
from simple_type_check import type_check, TypeCheckFailed

@type_check.returns
def id_(x) -> int:
    return x

_ = id_(1)  # Passes
try:
    _ = id_("string")  # Raises
except TypeCheckFailed as e:
    pass
```

Decorators for aruments exist as well: `type_check.args`.
Both can be done at once with `type_check.decorate`.

### With custom types

Basic types where `isinstance` is sufficient:
```python
from simple_type_check import TypeChecker

class Foo:
    pass

type_check = TypeChecker(Foo)

assert type_check(Foo(), Foo)
```

Special type checking logic desired:
```python
from simple_type_check import TopLevelCheck, TypeChecker

Bar = list[int] | list["Bar"]

class BarCheck(TopLevelCheck):
    def __call__(self, obj, type_) -> bool:
        return type_ == "Bar" and self._recurse(obj, Bar)

type_check = TypeChecker(advanced=[BarCheck])

type_check([1, [2], [[3]]], Bar)  # Should pass
```
This use case is useful for container types that take arguments, for example.
