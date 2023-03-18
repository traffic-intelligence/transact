from transact.transaction import Transaction, TransactionFailure
from transact.orchestrator import Orchestrator
from transact.job import Job


def do(job: Job):
    job.__setattr__("test", True)
    return True


def undo(job: Job):
    job.__setattr__("test", False)
    return True


def test_orchestrator_undo_failure():
    def fail(job: Job):
        raise TransactionFailure()

    success_transaction = Transaction(do, undo)
    failure_transaction = Transaction(fail, lambda x: True)

    orchestrator = Orchestrator([success_transaction, failure_transaction])
    job = Job()

    orchestrator.enqueue(job)

    assert job.__getattribute__("test") == False


def test_orchestrator_undo_false():
    def fail(job: Job):
        job.__setattr__("test2", True)
        return False

    def undo_fail(job: Job):
        job.__setattr__("test2", False)
        return True

    success_transaction = Transaction(do, undo)
    failure_transaction = Transaction(fail, undo_fail)

    orchestrator = Orchestrator([success_transaction, failure_transaction])
    job = Job()

    orchestrator.enqueue(job)

    assert job.__getattribute__("test") == False
    assert job.__getattribute__("test2") == False


def test_orchestrator_undo_job_failure():
    def fail(job: Job):
        job.failure = True
        return True

    def undo_fail(job: Job):
        job.__setattr__("test2", False)
        return True

    success_transaction = Transaction(do, undo)
    failure_transaction = Transaction(fail, undo_fail)

    orchestrator = Orchestrator([success_transaction, failure_transaction])
    job = Job()

    orchestrator.enqueue(job)

    assert job.__getattribute__("test") == False
    assert job.__getattribute__("test2") == False


def test_orchestrator_success():
    success_transaction = Transaction(do, undo)

    orchestrator = Orchestrator([success_transaction])
    job = Job()

    orchestrator.enqueue(job)

    assert job.__getattribute__("test")
