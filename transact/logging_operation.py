from enum import Enum
from logging import error, info, debug
from typing import Callable

from transact.operation import NoUndoOperation, NoDoOperation


class LoggingType(Enum):
    ERROR = "error"
    INFO = "info"
    DEBUG = "debug"


def _log(log_func: Callable, message: str):
    log_func(message)
    return True


class DoLoggingOperation(NoUndoOperation):

    def __init__(self, logging_type: LoggingType, message: str):
        if logging_type == LoggingType.ERROR:
            do_action = lambda x: _log(error, message)
        elif logging_type == LoggingType.INFO:
            do_action = lambda x: _log(info, message)
        elif logging_type == LoggingType.DEBUG:
            do_action = lambda x: _log(debug, message)
        else:
            do_action = lambda x: _log(print, message)

        super().__init__(do_action)


class UnDoLoggingOperation(NoDoOperation):

    def __init__(self, logging_type: LoggingType, message: str):
        if logging_type == LoggingType.ERROR:
            undo_action = lambda x: _log(error, message)
        elif logging_type == LoggingType.INFO:
            undo_action = lambda x: _log(info, message)
        elif logging_type == LoggingType.DEBUG:
            undo_action = lambda x: _log(debug, message)
        else:
            undo_action = lambda x: _log(print, message)

        super().__init__(undo_action)
