from typing import assert_never, assert_type, Never

import pytest

from cflow import (
    Some,
    Nothing,
    Option,
    OptionProtocol,
    Unit,
    UnpackingException,
)


def test_protocol_implementation():
    assert isinstance(Some(Unit()), OptionProtocol)
    assert isinstance(Nothing(), OptionProtocol)


def map_str_str(x: str) -> str:
    return f"{x}-2"


def map_str_int(x: str) -> int:
    return len(x)


def get_some_or_nothing(i: int) -> Option[str]:
    if i == 1:
        return Some("a")
    return Nothing()


def test_types_assertion():
    """The following tests check if the type checker can infer the correct
    types. To achieve this, errors are only fully detected when running
    the type checker over this file.

    The checks work by using assert_type, which will trigger general issues
    on runtime, and specific issues on type checker checks.
    """

    some_value = get_some_or_nothing(1)
    nothing = get_some_or_nothing(2)

    _ = assert_type(some_value, Option[str])
    _ = assert_type(nothing, Option[str])

    some_str = some_value.map(map_str_str)
    some_int = some_value.map(map_str_int)
    noth_str = nothing.map(map_str_str)
    noth_int = nothing.map(map_str_int)

    _ = assert_type(some_str, Option[str])
    _ = assert_type(some_int, Option[int])
    _ = assert_type(noth_str, Option[str])
    _ = assert_type(noth_int, Option[int])

    explicit_some = Some("a")
    explicit_some_map = explicit_some.map(map_str_str)

    _ = assert_type(explicit_some, Some[str])
    _ = assert_type(explicit_some_map, Some[str])

    expl_some_str = Some("a")
    expl_some_map_int = expl_some_str.map(map_str_int)

    _ = assert_type(expl_some_str, Some[str])
    _ = assert_type(expl_some_map_int, Some[int])

    expl_noth = Nothing()
    expl_noth_map = expl_noth.map(map_str_str)

    _ = assert_type(expl_noth, Nothing)
    _ = assert_type(expl_noth_map, Nothing)

    def assert_match_some_general[T](option: Option[T]):  # pyright: ignore[reportUnusedFunction]
        match option:
            case Some():
                assert True
            case Nothing():
                assert False
            case _:
                a = some_value
                _ = assert_type(a, Never)
                assert_never(some_value)

    def assert_match_some_value[T](option: Option[T], value: T):  # pyright: ignore[reportUnusedFunction]

        match option:
            case Some(val):
                a = val
                assert val == value
                _ = assert_type(val, T)
            case Nothing():
                assert False
            case _:
                a = some_value
                _ = assert_type(a, Never)
                assert_never(some_value)

    def assert_match_nothing[T](option: Option[T]): # pyright: ignore[reportUnusedFunction]
        match option:
            case Some():
                assert False
            case Nothing():
                assert True
            case _:
                a = some_value
                _ = assert_type(a, Never)
                assert_never(some_value)


def test_unwrap():
    some: Option[str] = get_some_or_nothing(1)
    nothing: Option[str] = get_some_or_nothing(2)

    unwraped_value: str = some.unwrap()
    assert unwraped_value == "a"

    with pytest.raises(UnpackingException):
        unwraped_value = nothing.unwrap()
        _ = assert_type(unwraped_value, str)


def test_for_unpacking():

    some: Option[str] = get_some_or_nothing(1)
    nothing: Option[str] = get_some_or_nothing(2)

    for value in some:
        assert value == "a"

    for value in nothing:
        assert False, "for iteration over Nothing should not work."
