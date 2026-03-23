from typing import assert_type, assert_never
from cflow import Some, Nothing, Option
from cflow._option import Skippable


def get_some_or_nothing(i: int) -> Option[str]:
    if i == 1:
        return Some("a")
    return Nothing()


def test_some_nothing_with():
    some: Some[int] = Some(1)
    with some.get_some() as val:
        assert val == 1

    with Skippable, some.get_some() as val:
        assert val == 1

    nothing: Nothing = Nothing()
    with Skippable, nothing.get_some() as val:
        assert False

    with Skippable, nothing.get_some() as val:
        assert_never(val)


def test_option_with():
    opt_some: Option[str] = get_some_or_nothing(1)
    opt_none: Option[str] = get_some_or_nothing(2)

    with Skippable, opt_some.get_some() as val:
        assert_type(val, str)
        assert val == "a"

    with Skippable, opt_none.get_some() as val:
        assert False


def assert_option[T](opt: Option[T]):
    with Skippable, opt.get_some() as val:
        assert_type(val, T)


def assert_option_explicit_type(opt: Option[str]):
    with Skippable, opt.get_some() as val:
        assert_type(val, str)


def assert_some[T](opt: Some[T]):
    with Skippable, opt.get_some() as val:
        assert_type(val, T)


def assert_some_explicit(opt: Some[str] = Some("a")):
    with Skippable, opt.get_some() as val:
        assert_type(val, str)
