from typing import Final

class _Skip(Exception):
    pass


class _Skippable:
    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_tp, *_):
        return exc_tp is not None and issubclass(exc_tp, _Skip)


Skippable: Final[_Skippable] = _Skippable()


class _ValueWith[T]:
    value: T

    def __init__(self, value: T):
        self.value = value

    def __enter__(self) -> T:
        return self.value

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass
