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

@type_checker.returns(int)
def id_(x):
    return x

_ = id_(1)  # Passes
try:
    id_("string")
except TypeCheckFailed as e:
    print("Bad input: ", e)
```

### With custom types

Basic types where `isinstance` is sufficient:
```python
from simple_type_checker import TypeChecker

class Foo:
    pass

type_check = TypeChecker(Foo)

assert type_checker(Foo(), Foo)
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

assert type_checker(Bad(True), Bar)
assert not type_checker(Bad(False), Bar)
```
This use case is useful for container types that take arguments, for example.
