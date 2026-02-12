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
    Final,
)

from overt._error import UnpackingException
from overt._skippable import _Skip, Skippable, _ValueWith, _Skippable


T = TypeVar("T")
S = TypeVar("S")


type _MapFunc[T, S] = Callable[[T], S]


@runtime_checkable
class OptionProtocol[T](Protocol):
    value: T | None

    def map[S](self, func: _MapFunc[T, S]) -> OptionProtocol[S]: ...
    def map_or[S](
        self, func: _MapFunc[T, S], default: S
    ) -> OptionProtocol[S]: ...
    def is_some(self) -> bool: ...
    def is_nothing(self) -> bool: ...
    def unwrap(self) -> T: ...
    def get_some(self) -> _ValueWith[T]: ...


def is_some[T](obj: Option[T]) -> TypeGuard[Some[T]]:
    return obj.is_some()


def is_nothing[T](obj: Option[T]) -> TypeGuard[Nothing]:
    return obj.is_nothing()


@final
class Some[T](OptionProtocol[T]):
    value: T

    __slots__: tuple[Literal["value"]] = ("value",)
    __match_args__: tuple[Literal["value"]] = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def map[S](self, func: _MapFunc[T, S]) -> Some[S]:
        new_value: S = func(self.value)
        return Some(new_value)

    def map_or[S](self, func: _MapFunc[T, S], default: S) -> Some[S]:
        return self.map(func)

    def is_some(self) -> Literal[True]:
        return True

    def is_nothing(self) -> Literal[False]:
        return False

    def unwrap(self) -> T:
        return self.value

    def get_some(self) -> _ValueWith[T]:
        return _ValueWith(self.value)


@final
class Nothing(OptionProtocol):
    Skip: Final[_Skippable] = Skippable

    slots: tuple[()] = ()
    __match_args__: tuple[()] = ()

    def map[T, S](cls, func: _MapFunc[T, S]) -> Nothing:
        return Nothing()

    def map_or[T, S](self, func: _MapFunc[T, S], default: S) -> Nothing:
        return Nothing()

    def is_some(self) -> Literal[False]:
        return False

    def is_nothing(self) -> Literal[True]:
        return True

    def unwrap(self) -> NoReturn:
        raise UnpackingException("Nothing value was unpacked.")

    def get_some(self) -> NoReturn:
        raise _Skip


type Option[T] = Some[T] | Nothing
