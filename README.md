# cflow - Explicit Python

## Architecture

* All classes / functions are re-exported to the packages `__init__.py`

--> There is only one place to import everything

```python
from cflow import Option, Unit
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
- Type-checking: `ty`

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
| `mypy`         | &cross;       | &quest; Don't wanna deal with stub-files.                                  |

### ty

* `ty =< 0.0.16` currently does not infer the type of an unpacked value
  in a match statement

```python
from typing import assert_type, assert_never
from cflow import Option

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
from cflow import Option

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
