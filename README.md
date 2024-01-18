# simple\_type\_checker

A small extendable python type checker library

### Basic Usage

Checking a type:
```python
from simple_type_checker import type_check
assert type_check("A string", str)
```

As a decorator:
```python
from simple_type_checker import type_check, TypeCheckFailed

@type_check.returns
def id_(x) -> int:
    return x

_ = id_(1)  # Passes
try:
    id_("string")
except TypeCheckFailed as e:
    print("Bad input: ", e)
```

Decorators for aruments exist as well: `type_check.args`. Both can be done at once with `type_check.decorate`.

### With custom types

Basic types where `isinstance` is sufficient:
```python
from simple_type_checker import TypeChecker

class Foo:
    pass

type_check = TypeChecker(Foo)

assert type_check(Foo(), Foo)
```

Special type checking logic desired
```python
from simple_type_checker import TypeChecker, Checker

class Bar:
    def __init__(self, b):
        self.can_check = b

class CheckerBar(Checker):
    def __call__(self, obj: Any, type_: Any) -> bool:
        return type_ == Bar and isinstance(obj, Bar) and obj.can_check

type_check = TypeChecker(advanced=(Bar,))

assert type_check(Bad(True), Bar)
assert not type_check(Bad(False), Bar)
```
This use case is useful for container types that take arguments, for example.
