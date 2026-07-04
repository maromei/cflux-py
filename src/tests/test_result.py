from typing import assert_type, assert_never

import pytest

from cflow import (
    Ok,
    Err,
    Result,
    ResultProtocol,
    Unit,
    UnpackingException,
    is_ok,
    is_err,
)


def assert_exception_equal(ex1: BaseException, ex2: BaseException):
    assert type(ex1) is type(ex2)
    assert ex1.args == ex2.args


class CustomTestException(Exception):
    pass


def get_ok_or_err(i: int) -> Result[int, CustomTestException]:
    if i == 1:
        return Ok(1)
    return Err(CustomTestException(str(i)))


def test_protocol_implementation():
    assert isinstance(Ok(Unit()), ResultProtocol)
    assert isinstance(Err(Unit()), ResultProtocol)


def test_assert_type():
    ok = get_ok_or_err(1)
    err = get_ok_or_err(2)

    _ = assert_type(ok, Result[int, CustomTestException])
    _ = assert_type(err, Result[int, CustomTestException])

    explicit_ok = Ok(11)
    explicit_err = Err(CustomTestException("22"))

    _ = assert_type(explicit_ok, Ok[int])
    _ = assert_type(explicit_err, Err[CustomTestException])


def test_match():
    ok = get_ok_or_err(1)
    err = get_ok_or_err(2)

    match ok:
        case Ok():
            assert True
        case Err():
            assert False
        case _:
            assert_never(ok)

    match err:
        case Ok():
            assert False
        case Err():
            assert True
        case _:
            assert_never(err)

    # Now lets do the same but we capture the value contained

    # we re-assign the values since the type checkers have already figured out
    # that the values are Ok or Err via type narrowing and the match statements above
    ok = get_ok_or_err(1)
    err = get_ok_or_err(2)

    match ok:
        case Ok(val):
            assert val == ok.value
            _ = assert_type(val, int)
        case Err():
            assert False
        case _:
            assert_never(ok)

    match err:
        case Ok():
            assert False
        case Err(err_val):
            assert err_val == err.value
            _ = assert_type(err_val, CustomTestException)
        case _:
            assert_never(err)


def test_unwrap():
    ok = Ok(1)
    err = Err(CustomTestException("hello"))

    assert ok.unwrap() == 1
    with pytest.raises(UnpackingException):
        _ = err.unwrap()

    assert ok.unwrap_or_raise() == 1
    with pytest.raises(CustomTestException):
        _ = err.unwrap_or_raise()


def test_map():
    def map_int_str(some_int: int) -> str:
        return str(some_int)

    def map_to_other_exception(exc: CustomTestException) -> ValueError:
        return ValueError(exc)

    err_value = CustomTestException("hello")
    new_err_value = ValueError(err_value)

    ok_value = 1
    new_ok_value = str(ok_value)

    ok = Ok(ok_value)
    err = Err(err_value)

    ok2 = ok.map(map_int_str)
    assert ok.unwrap() == ok_value
    assert ok2.unwrap() == new_ok_value

    ok3 = ok.map_err(map_to_other_exception)
    assert ok.unwrap() == ok_value
    assert ok3.unwrap() == ok_value

    err2 = err.map(map_to_other_exception)
    assert_exception_equal(err.get(), err_value)
    assert_exception_equal(err2.get(), err_value)

    err3 = err.map_err(map_to_other_exception)
    assert_exception_equal(err.get(), err_value)
    assert_exception_equal(err3.get(), new_err_value)


def test_get():
    ok_value = 1
    err_value = CustomTestException("hello")
    ok = Ok(ok_value)
    err = Err(err_value)

    assert ok.get() == ok_value
    assert_exception_equal(err.get(), err.value)


def test_and_then():
    def and_then_ok(i: int) -> Result[str, ValueError]:
        return Ok(str(i + 1))

    def and_then_err(i: int) -> Result[int, ValueError]:  # pyright: ignore[reportUnusedParameter]
        return Err(ValueError(2))

    ok = get_ok_or_err(1)
    err = get_ok_or_err(2)
    err_value = CustomTestException("2")

    ok2 = ok.and_then(and_then_ok)
    assert ok.get() == 1
    assert ok2.get() == "2"
    assert ok2.is_ok()

    ok3 = ok.and_then(and_then_err)
    assert ok.get() == 1
    if is_err(ok3):
        assert_exception_equal(ok3.get(), ValueError(2))
    else:
        assert False

    err2 = err.and_then(and_then_ok)
    if is_err(err):
        assert_exception_equal(err.get(), err_value)
    else:
        assert False
    if is_err(err2):
        assert_exception_equal(err2.get(), err_value)
    else:
        assert False

    err3 = err.and_then(and_then_err)
    if is_err(err):
        assert_exception_equal(err.get(), err_value)
    else:
        assert False
    if is_err(err3):
        assert_exception_equal(err3.get(), err_value)
    else:
        assert False


def test_for_loop_unpacking():
    ok = get_ok_or_err(1)
    err = get_ok_or_err(2)

    was_called: bool = False
    for ok_val in ok:
        was_called = True
        assert ok_val == 1
    assert was_called

    was_called = False
    for err_val in err:
        assert False
    assert not was_called
