from typing import Callable, Any
from logging import warning

from transact.operation import NoUndoOperation, NoDoOperation
from transact.job import Job


def no_undo_operation(func: Callable[[Any], bool]) -> NoUndoOperation:

    def do_action(job: Job):
        kwargs = {}
        for key in func.__code__.co_varnames:
            if key == "job":
                kwargs[key] = job
                continue

            try:
                kwargs[key] = job.__getattribute__(key)
            except AttributeError:
                warning(f'Ignoring attribute {key} because not in job {job}')

        return func(**kwargs)

    return NoUndoOperation(do_action)


def no_do_operation(func: Callable[[Any], bool]) -> NoDoOperation:

    def undo_action(job: Job):
        kwargs = {}
        for key in func.__code__.co_varnames:
            if key == "job":
                kwargs[key] = job
                continue

            try:
                kwargs[key] = job.__getattribute__(key)
            except AttributeError:
                warning(f'Ignoring attribute {key} because not in job {job}')

        return func(**kwargs)

    return NoDoOperation(undo_action)
