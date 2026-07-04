from __future__ import annotations
from typing import (
    Callable,
    Protocol,
    final,
    Literal,
    runtime_checkable,
    TypeGuard,
    TypeVar,
    NoReturn,
    Never,
)
from collections.abc import Iterator

from cflow._error import UnpackingException


T = TypeVar("T")
S = TypeVar("S")


type _MapFunc[T, S] = Callable[[T], S]


@runtime_checkable
class OptionProtocol[T](Protocol):
    def map[S](self, func: _MapFunc[T, S]) -> OptionProtocol[S]: ...
    def map_or[S](self, func: _MapFunc[T, S], default: S) -> OptionProtocol[S]: ...
    def is_some(self) -> bool: ...
    def is_nothing(self) -> bool: ...
    def unwrap(self) -> T: ...
    def unwrap_or[S](self, default: S) -> T | S: ...
    def __iter__(self) -> Iterator[T]: ...


def is_some[T](obj: Option[T]) -> TypeGuard[Some[T]]:
    return obj.is_some()


def is_nothing[T](obj: Option[T]) -> TypeGuard[Nothing]:
    return obj.is_nothing()


@final
class Some[T]:
    value: T

    __slots__: tuple[Literal["value"]] = ("value",)
    __match_args__: tuple[Literal["value"]] = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def map[S](self, func: _MapFunc[T, S]) -> Some[S]:
        new_value: S = func(self.value)
        return Some(new_value)

    def map_or[S](self, func: _MapFunc[T, S], default: S) -> Some[S]:  # pyright: ignore[reportUnusedParameter]
        return self.map(func)

    def is_some(self) -> Literal[True]:
        return True

    def is_nothing(self) -> Literal[False]:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or[S](self, default: S) -> T:  # pyright: ignore[reportUnusedParameter, reportInvalidTypeVarUse]
        return self.value

    def __iter__(self) -> Iterator[T]:
        yield self.value


@final
class Nothing:
    slots: tuple[()] = ()
    __match_args__: tuple[()] = ()

    def map[T, S](self, func: _MapFunc[T, S]) -> Nothing:  # pyright: ignore[reportUnusedParameter]
        return Nothing()

    def map_or[T, S](self, func: _MapFunc[T, S], default: S) -> S:  # pyright: ignore[reportUnusedParameter]
        return default

    def is_some(self) -> Literal[False]:
        return False

    def is_nothing(self) -> Literal[True]:
        return True

    def unwrap(self) -> NoReturn:
        raise UnpackingException("Nothing value was unpacked.")

    def unwrap_or[S](self, default: S) -> S:
        return default

    def __iter__(self) -> Iterator[Never]:
        return
        yield  # dummy yield statement  # pyright: ignore[reportUnreachable]


type Option[T] = Some[T] | Nothing
