from cflow._option import Some as Some
from cflow._option import Nothing as Nothing
from cflow._option import Option as Option
from cflow._option import OptionProtocol as OptionProtocol
from cflow._option import is_some as is_some
from cflow._option import is_nothing as is_nothing

from cflow._result import Result as Result
from cflow._result import Ok as Ok
from cflow._result import Err as Err
from cflow._result import ResultProtocol as ResultProtocol
from cflow._result import is_ok as is_ok
from cflow._result import is_err as is_err

from cflow._unit import Unit as Unit

from cflow._error import CflowException as CflowException
from cflow._error import UnpackingException as UnpackingException
from cflow._error import ExpectedException as ExpectedException

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
    "CflowException",
    "UnpackingException",
    "ExpectedException",
]
