from typing import Callable
from logging import error

from transact.job import Job


class Operation:

    def __init__(self, action: Callable[[Job], bool], undo_action: Callable[[Job], bool], retry: int = 0):
        self._action = action
        self._undo_action = undo_action
        self._retry = retry

    def do(self, job: Job) -> bool:
        for i in range(self._retry):
            try:
                success = self._action(job)

                if job.failure or not success:
                    raise OperationFailure()

                return success
            except Exception as e:
                error(f'Failed to do job {job} in transaction {self} for retry {i} because {e}')

        return self._action(job)

    def undo(self, job: Job):
        return self._undo_action(job)


class NoUndoOperation(Operation):

    def __init__(self, action: Callable[[Job], bool], retry: int = 0):
        super().__init__(action, lambda x: True, retry)


class NoDoOperation(Operation):
    def __init__(self, undo_action: Callable[[Job], bool], retry: int = 0):
        super().__init__(lambda x: True, undo_action, retry)


class OperationFailure(Exception):
    def __init__(self):
        super().__init__("Transaction failed")
