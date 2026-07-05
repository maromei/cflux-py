# cflux - Control Flow Objects for Python

## Features

### Option Type

* Represent optional values, freeing `None` to be a usable value.
  ```python
  from cflux import Option, Some, Nothing
  val: Option[int] = Some(42)
  empty: Option[int] = Nothing()
  ```

* **Pattern Matching**: Destructure option.
  ```python
  match val:
      case Some(x):
          print(x)
      case Nothing():
          print("Empty")
  ```

* **Functional Methods**: Transform inner values.
  ```python
  val.map(lambda x: x * 2)  # Some(84)
  empty.map_or(lambda x: x * 2, 0)  # 0
  ```

* **Unwrapping**: Extract inner value.
  ```python
  x: int = val.unwrap()  # 42
  empty.unwrap()  # raises UnpackingException
  y: int = empty.unwrap_or(0)  # 0
  ```

* **For Loop unpacking**: Run code in a block if the value is some, using for loops
  ```python
  some: Option[str] = Some("a")
  nothing: Option[str] = Nothing()

  for value in some:
      print("This messag will be printed.")

  for value in nothing:
      print("This message will not be printed.")
  ```

### Result Type

* Represent success or error values.
  ```python
  from cflux import Result, Ok, Err
  success: Result[int, str] = Ok(42)
  failure: Result[int, str] = Err("Error message")
  ```

* **Pattern Matching**: Destructure result.
  ```python
  match success:
      case Ok(x):
          print(x)
      case Err(err):
          print(err)
  ```

* **Functional Methods**: Transform inner values.
  ```python
  success.map(lambda x: x * 2)  # Ok(84)
  failure.map_err(lambda err: f"Error: {err}")  # Err("Error: Error message")
  ```

* **Unwrapping**: Extract inner value.
  ```python
  x: int = success.unwrap()  # 42
  failure.unwrap()  # raises UnpackingException
  failure.unwrap_or_raise()  # raises wrapped exception
  y: int = failure.unwrap_or(0)  # 0
  ```

* **For Loop unpacking**: Run code in a block if the value is ok, using for loops.
  ```python
  success: Result[str, int] = Ok("a")
  failure: Result[str, int] = Err(1)

  for value in success:
      print("This message will be printed.")

  for value in failure:
      print("This message will not be printed.")
  ```

## Architecture

* All classes / functions are re-exported to the packages `__init__.py`

--> There is only one place to import everything

```python
from cflux import Option, Unit
```

* The actual definitions are done in private modules. F.e `_options.py`

## Development Environment

### Dependencies

- `uv`: Install from here:
  [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### Environment Setup

On every session start, call:

```bash
source env
```

* Adds relative directory `scripts/` to `PATH`
* Calls `scripts/setup` and checks for system dependecies
* Creates `.venv` and syncs dependencies

On the first startup, this should setup the dev environment completely.
Otherwise you can call `scripts/setup` manually.

### Development Tools

- Linting: `ruff`
- Type-checking: `basedpyright`

### Internal Dev Commands

Some Commands that might be useful:

* `style-check`: Runs linter and type checker
* `style-format`: Runs formatter
* `test-all`: Run the tests.
    * The tests contain calls to other typecheckers. This can be skipped
      by passing the `--skip-typing` flag.
    * Use the `test-all --help` command for more information.

## Supported Type Checker

While `ty` is mainly used during the development, the tests also run
additional typecheckers to see how the type-inference works.
<br>
The following table contains a summary of the support.
Some type checkerr have additional information in a subsection below.

| type checker   | is tested for | functionality                                                              |
| -------------- | ------------- | -------------------------------------------------------------------------- |
| `ty`           | &check;       | Missing feature in `ty` for match value unpacking.                         |
| `pyrefly`      | &check;       | Failing the exhaustiveness checks in the match statement.                  |
| `pyright`      | &check;       | &check; + Non-speced feature: Complain on `Nothing` in a `with` statement. |
| `basedpyright` | &check;       | &quest; + Non-speced feature: Complain on `Nothing` in a `with` statement. |
| `mypy`         | &cross;       | &quest;                                                                    |

### ty

* `ty =< 0.0.16` currently does not infer the type of an unpacked value
  in a match statement

```python
from typing import assert_type, assert_never
from cflux import Option

# snip...: some code that sets some_value

some_value: Option[int]

match some_value:
    case Some(unpacked_value):
        # ty will complain here
        # its infered type is @Todo
        assert_type(unpacked_value, int)
    case Nothing():
        pass
    case _:
        assert_never(some_value)
```

There is a test that will test this case. It will currently always fail.
<br>
A workaround requires the `typing.cast` function. Simply adding the typehint
`unpacked_value: int` will not work.

```python
from typing import assert_type, assert_never, cast
from cflux import Option

# snip...: some code that sets some_value

some_value: Option[int]

match some_value:
    case Some(unpacked_value):
        unpacked_value = cast(int, unpacked_value)
        assert_type(unpacked_value, int)
    case Nothing():
        pass
    case _:
        assert_never(some_value)
```

This has the drawback of not giving a typeerror when the `some_value`
ever switches in type.
