from typing import List
from logging import error, info

from transact.transaction import Transaction, TransactionFailure
from transact.job import Job


class Orchestrator:

    def __init__(self, transactions: List[Transaction]):
        self._transactions = transactions

    def enqueue(self, job: Job):
        for i, transaction in enumerate(self._transactions):
            try:
                success = transaction.do(job)
                if not success or job.failure:
                    raise TransactionFailure()
            except Exception as e:
                error(f'orchestrator failed to do transaction {transaction} at index {i} for job {job} '
                      f'with exception {e}')
                self.undo_all(job, i)

    def undo_all(self, job: Job, index: int):
        while index >= 0:
            current_transaction = self._transactions[index]

            try:
                current_transaction.undo(job)
            except Exception as e:
                error(f'orchestrator failed undo transaction {current_transaction} at index {index} for job {job} '
                      f'with exception {e}')

            index -= 1
