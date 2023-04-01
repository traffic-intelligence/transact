from typing import Callable, Any
from logging import warning
from inspect import signature

from transact.operation import NoUndoOperation, NoDoOperation
from transact.job import Job


def no_undo_operation(num_retry: int = 0) -> Callable[[Callable[[Any], bool]], NoUndoOperation]:
    def _decorator(func: Callable[[Any], bool]) -> NoUndoOperation:

        def do_action(job: Job):
            kwargs = {}
            for key in signature(func).parameters:
                if key == "job":
                    kwargs[key] = job
                    continue

                try:
                    kwargs[key] = job.__getattribute__(key)
                except AttributeError:
                    warning(f'Ignoring attribute {key} because not in job {job}')

            return func(**kwargs)

        return NoUndoOperation(do_action, retry=num_retry)
    return _decorator


def no_do_operation(num_retry: int = 0) -> Callable[[Callable[[Any], bool]], NoDoOperation]:
    def _decorator(func: Callable[[Any], bool]) -> NoDoOperation:
        def undo_action(job: Job):
            kwargs = {}
            for key in signature(func).parameters:
                if key == "job":
                    kwargs[key] = job
                    continue

                try:
                    kwargs[key] = job.__getattribute__(key)
                except AttributeError:
                    warning(f'Ignoring attribute {key} because not in job {job}')

            return func(**kwargs)

        return NoDoOperation(undo_action, retry=num_retry)
    return _decorator