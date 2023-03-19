from transact.job import Job
from transact.operation import Operation, NoUndoOperation, OperationFailure


def do(job: Job):
    job.__setattr__("test", True)
    return True


def undo(job: Job):
    job.__setattr__("test", False)
    return True


def test_operation_do_undo():
    operation = Operation(do, undo)
    job = Job()

    operation.do(job)
    assert job.__getattribute__("test")

    operation.undo(job)
    assert not job.__getattribute__("test")


def test_operation_retry():
    def inc_counter(job: Job):
        comp = job.counter == 2
        job.counter += 1
        return comp

    job = Job()
    job.__setattr__("counter", 0)

    operation = NoUndoOperation(inc_counter, 2)

    operation.do(job)
    assert job.counter == 3


def test_operation_retry_fail():
    def inc_counter(job: Job):
        comp = job.counter == 2
        job.counter += 1
        return comp

    job = Job()
    job.__setattr__("counter", 0)

    operation = NoUndoOperation(inc_counter, 1)

    success = operation.do(job)
    assert not success


def test_operation_retry_fail_exception():
    def inc_counter(job: Job):
        job.counter += 1
        raise OperationFailure()

    job = Job()
    job.__setattr__("counter", 0)

    operation = NoUndoOperation(inc_counter, 1)
    try:
        success = operation.do(job)
        assert not success
    except OperationFailure as e:
        assert True
        assert job.counter == 2
    except Exception as e:
        print(f'test failed because {e}')
        assert False