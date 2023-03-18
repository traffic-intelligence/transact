from typing import Callable
from logging import error

from transact.job import Job


class Transaction:

    def __init__(self, action: Callable[[Job], bool], undo_action: Callable[[Job], bool], retry: int = 0):
        self._action = action
        self._undo_action = undo_action
        self._retry = retry

    def do(self, job: Job) -> bool:
        for i in range(self._retry):
            try:
                success = self._action(job)

                if job.failure or not success:
                    raise TransactionFailure()

                return success
            except Exception as e:
                error(f'Failed to do job {job} in transaction {self} for retry {i} because {e}')

        return self._action(job)

    def undo(self, job: Job):
        return self._undo_action(job)


class NoUndoTransaction(Transaction):

    def __init__(self, action: Callable[[Job], bool], retry: int = 0):
        super().__init__(action, lambda x: True, retry)


class NoDoTransaction(Transaction):
    def __init__(self, undo_action: Callable[[Job], bool], retry: int = 0):
        super().__init__(lambda x: True, undo_action, retry)


class TransactionFailure(Exception):
    def __init__(self):
        super().__init__("Transaction failed")
