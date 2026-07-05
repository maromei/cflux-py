from cflux._option import Some as Some
from cflux._option import Nothing as Nothing
from cflux._option import Option as Option
from cflux._option import OptionProtocol as OptionProtocol
from cflux._option import is_some as is_some
from cflux._option import is_nothing as is_nothing

from cflux._result import Result as Result
from cflux._result import Ok as Ok
from cflux._result import Err as Err
from cflux._result import ResultProtocol as ResultProtocol
from cflux._result import is_ok as is_ok
from cflux._result import is_err as is_err

from cflux._unit import Unit as Unit

from cflux._error import CfluxException as CfluxException
from cflux._error import UnpackingException as UnpackingException
from cflux._error import ExpectedException as ExpectedException

__all__ = [
    "Some",
    "Nothing",
    "Option",
    "OptionProtocol",
    "Result",
    "ResultProtocol",
    "Ok",
    "Err",
    "is_ok",
    "is_err",
    "is_some",
    "is_nothing",
    "Unit",
    "CfluxException",
    "UnpackingException",
    "ExpectedException",
]
