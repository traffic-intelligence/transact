from transact.job import Job
from transact.transaction import Transaction, NoUndoTransaction, TransactionFailure


def do(job: Job):
    job.__setattr__("test", True)
    return True


def undo(job: Job):
    job.__setattr__("test", False)
    return True


def test_transaction_do_undo():
    transaction = Transaction(do, undo)
    job = Job()

    transaction.do(job)
    assert job.__getattribute__("test")

    transaction.undo(job)
    assert not job.__getattribute__("test")


def test_transaction_retry():
    def inc_counter(job: Job):
        comp = job.counter == 2
        job.counter += 1
        return comp

    job = Job()
    job.__setattr__("counter", 0)

    transaction = NoUndoTransaction(inc_counter, 2)

    transaction.do(job)
    assert job.counter == 3


def test_transaction_retry_fail():
    def inc_counter(job: Job):
        comp = job.counter == 2
        job.counter += 1
        return comp

    job = Job()
    job.__setattr__("counter", 0)

    transaction = NoUndoTransaction(inc_counter, 1)

    success = transaction.do(job)
    assert not success


def test_transaction_retry_fail_exception():
    def inc_counter(job: Job):
        job.counter += 1
        raise TransactionFailure()

    job = Job()
    job.__setattr__("counter", 0)

    transaction = NoUndoTransaction(inc_counter, 1)
    try:
        success = transaction.do(job)
        assert not success
    except TransactionFailure as e:
        assert True
        assert job.counter == 2
    except Exception as e:
        print(f'test failed because {e}')
        assert False