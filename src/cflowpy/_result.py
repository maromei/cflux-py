from __future__ import annotations
from typing import (
    Any,
    NoReturn,
    Protocol,
    TypeGuard,
    final,
    Literal,
    Never,
    runtime_checkable,
    Callable,
    Generic,
    TypeVar,
)
from collections.abc import Iterator


from cflowpy._error import UnpackingException


type _MapFunc[T, S] = Callable[[T], S]
type _FuncResult[T, U, V] = Callable[[T], Result[U, V]]


@runtime_checkable
class ResultProtocol[ValType, ErrType](Protocol):
    def map[NewValType](
        self, func: _MapFunc[ValType, NewValType]
    ) -> ResultProtocol[NewValType, ErrType]: ...
    def map_err[NewErrType](
        self, func: _MapFunc[ErrType, NewErrType]
    ) -> ResultProtocol[ValType, NewErrType]: ...
    def and_then[NewValType, NewErrType](
        self, func: _FuncResult[ValType, NewValType, NewErrType]
    ) -> Result[NewValType, ErrType | NewErrType]: ...
    def unwrap(self) -> ValType: ...
    def unwrap_or_raise(self) -> ValType: ...
    def unwrap_or[NewValType](self, default: NewValType) -> ValType | NewValType: ...
    def get(self) -> ValType | ErrType: ...
    def is_ok(self) -> bool: ...
    def is_err(self) -> bool: ...
    def __iter__(self) -> Iterator[ValType]: ...


def is_ok[S, T](obj: Result[S, T]) -> TypeGuard[Ok[S]]:
    return obj.is_ok()


def is_err[S, T](obj: Result[S, T]) -> TypeGuard[Err[T]]:
    return obj.is_err()


ValType_co = TypeVar("ValType_co", covariant=True)
ErrType_co = TypeVar("ErrType_co", covariant=True)


@final
class Ok(Generic[ValType_co]):
    value: ValType_co

    __slots__: tuple[Literal["value"]] = ("value",)
    __match_args__: tuple[Literal["value"]] = ("value",)

    def __init__(self, value: ValType_co) -> None:
        self.value = value

    def map[NewValType](self, func: _MapFunc[ValType_co, NewValType]) -> Ok[NewValType]:
        return Ok(func(self.value))

    def map_err[ErrType, NewErrType](
        self,
        func: _MapFunc[ErrType, NewErrType],  # pyright: ignore[reportUnusedParameter]
    ) -> Ok[ValType_co]:
        return Ok(self.value)

    def and_then[NewValType, NewErrType](
        self, func: _FuncResult[ValType_co, NewValType, NewErrType]
    ) -> Result[NewValType, NewErrType]:
        return func(self.value)

    def unwrap(self) -> ValType_co:
        return self.value

    def unwrap_or_raise(self) -> ValType_co:
        return self.value

    def unwrap_or[NewValType](self, default: NewValType) -> ValType_co:  # pyright: ignore[reportUnusedParameter, reportInvalidTypeVarUse]
        return self.value

    def get(self) -> ValType_co:
        return self.value

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def __iter__(self) -> Iterator[ValType_co]:
        yield self.value


@final
class Err(Generic[ErrType_co]):
    value: ErrType_co

    __slots__: tuple[Literal["value"]] = ("value",)
    __match_args__: tuple[Literal["value"]] = ("value",)

    def __init__(self, err: ErrType_co) -> None:
        self.value = err

    def map[ValType, NewValType](
        self,
        func: _MapFunc[ValType, NewValType],  # pyright: ignore[reportUnusedParameter]
    ) -> Err[ErrType_co]:
        return Err(self.value)

    def map_err[NewErrType](
        self, func: _MapFunc[ErrType_co, NewErrType]
    ) -> Err[NewErrType]:
        return Err(func(self.value))

    def and_then[ValType, NewValType, NewErrType](
        self,
        func: _FuncResult[ValType, NewValType, NewErrType],  # pyright: ignore[reportUnusedParameter]
    ) -> Err[ErrType_co]:
        return Err(self.value)

    def unwrap(self) -> NoReturn:
        def check_exception(obj: Any) -> TypeGuard[BaseException]:  # pyright: ignore[reportAny]
            return isinstance(obj, BaseException)

        if check_exception(self.value):
            raise UnpackingException("Unpacking error") from self.value
        raise UnpackingException("Unpacking error: " + str(self.value))

    def unwrap_or_raise(self) -> NoReturn:
        def check_exception(obj: Any) -> TypeGuard[BaseException]:  # pyright: ignore[reportAny]
            return isinstance(obj, BaseException)

        if check_exception(self.value):
            raise self.value
        raise UnpackingException("Unpacking error: " + str(self.value))

    def unwrap_or[NewValType](self, default: NewValType) -> NewValType:
        return default

    def get(self) -> ErrType_co:
        return self.value

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def __iter__(self) -> Iterator[Never]:
        return
        yield  # dummy yield # pyright: ignore[reportUnreachable]


type Result[ValType, ErrType] = Ok[ValType] | Err[ErrType]
