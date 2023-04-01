from typing import List
from logging import error, info

from transact.operation import Operation, OperationFailure
from transact.job import Job


class Transaction:

    def __init__(self, operations: List[Operation]):
        self._operations = operations

    def enqueue(self, job: Job) -> bool:
        for i, operation in enumerate(self._operations):
            try:
                success = operation.do(job)
                if not success or job.failure:
                    raise OperationFailure()
            except Exception as e:
                error(f'transaction failed to do operation {operation} at index {i} for job {job} '
                      f'with exception {e}')
                return self.undo_all(job, i)

        return True

    def undo_all(self, job: Job, index: int) -> bool:
        while index >= 0:
            current_operation = self._operations[index]

            try:
                current_operation.undo(job)
            except Exception as e:
                error(f'transaction failed undo operation {current_operation} at index {index} for job {job} '
                      f'with exception {e}')

            index -= 1

        return False
