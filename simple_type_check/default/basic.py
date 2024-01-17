from types import NoneType, EllipsisType
from sys import version_info
from pathlib import Path
import numbers


__all__ = ("BASIC",)


_BUILTIN_PRIMITIVES: set[type] = {
    NoneType,
    EllipsisType,
    object,
    str,
    int,
    float,
    complex,
    bool,
    bytes,
    type,
    range,
    bytearray,
    memoryview,
    frozenset,
    NotImplemented,
}

_PRIMITIVES: set[type] = {
    Path,
}

_NUMBERS: set[type] = {
    numbers.Integral,
    numbers.Rational,
    numbers.Complex,
    numbers.Real,
}

_EXCEPTIONS: set[type] = {
    BaseException,
    GeneratorExit,
    KeyboardInterrupt,
    SystemExit,
    Exception,
    ArithmeticError,
    FloatingPointError,
    OverflowError,
    ZeroDivisionError,
    AssertionError,
    AttributeError,
    BufferError,
    EOFError,
    ImportError,
    ModuleNotFoundError,
    LookupError,
    IndexError,
    KeyError,
    MemoryError,
    NameError,
    UnboundLocalError,
    OSError,
    BlockingIOError,
    ChildProcessError,
    ConnectionError,
    BrokenPipeError,
    ConnectionAbortedError,
    ConnectionRefusedError,
    ConnectionResetError,
    FileExistsError,
    FileNotFoundError,
    InterruptedError,
    IsADirectoryError,
    NotADirectoryError,
    PermissionError,
    ProcessLookupError,
    TimeoutError,
    ReferenceError,
    RuntimeError,
    NotImplementedError,
    RecursionError,
    StopAsyncIteration,
    StopIteration,
    SyntaxError,
    IndentationError,
    TabError,
    SystemError,
    TypeError,
    ValueError,
    UnicodeError,
    UnicodeDecodeError,
    UnicodeEncodeError,
    UnicodeTranslateError,
    Warning,
    BytesWarning,
    DeprecationWarning,
    EncodingWarning,
    FutureWarning,
    ImportWarning,
    PendingDeprecationWarning,
    ResourceWarning,
    RuntimeWarning,
    SyntaxWarning,
    UnicodeWarning,
    UserWarning,
}

BASIC: set[type] = _BUILTIN_PRIMITIVES | _PRIMITIVES | _NUMBERS | _EXCEPTIONS

if version_info >= (3, 11):
    # pylint: disable=undefined-variable
    BASIC |= {BaseExceptionGroup, ExceptionGroup}  # type: ignore
