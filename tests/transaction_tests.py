from transact.operation import Operation, OperationFailure
from transact.transaction import Transaction
from transact.job import Job


def do(job: Job):
    job.__setattr__("test", True)
    return True


def undo(job: Job):
    job.__setattr__("test", False)
    return True


def test_transaction_undo_failure():
    def fail(job: Job):
        raise OperationFailure()

    success_operation = Operation(do, undo)
    failure_operation = Operation(fail, lambda x: True)

    transaction = Transaction([success_operation, failure_operation])
    job = Job()

    success = transaction.enqueue(job)

    assert job.__getattribute__("test") == False
    assert not success


def test_transaction_undo_false():
    def fail(job: Job):
        job.__setattr__("test2", True)
        return False

    def undo_fail(job: Job):
        job.__setattr__("test2", False)
        return True

    success_operation = Operation(do, undo)
    failure_operation = Operation(fail, undo_fail)

    transaction = Transaction([success_operation, failure_operation])
    job = Job()

    success = transaction.enqueue(job)

    assert job.__getattribute__("test") == False
    assert job.__getattribute__("test2") == False
    assert not success


def test_transaction_undo_job_failure():
    def fail(job: Job):
        job.failure = True
        return True

    def undo_fail(job: Job):
        job.__setattr__("test2", False)
        return True

    success_operation = Operation(do, undo)
    failure_operation = Operation(fail, undo_fail)

    transaction = Transaction([success_operation, failure_operation])
    job = Job()

    success = transaction.enqueue(job)

    assert job.__getattribute__("test") == False
    assert job.__getattribute__("test2") == False
    assert not success


def test_transaction_success():
    success_operation = Operation(do, undo)

    transaction = Transaction([success_operation])
    job = Job()

    success = transaction.enqueue(job)

    assert job.__getattribute__("test")
    assert success
