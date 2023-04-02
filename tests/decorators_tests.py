from transact.decorators import no_undo_operation, no_do_operation
from transact.job import Job


def test_no_undo_operation_decorator():

    @no_undo_operation()
    def test_func(test):
        assert test == "test"
        return True

    job = Job(test="test")

    test_func.do(job)


def test_no_do_operation_decorator():

    @no_do_operation()
    def test_func(test):
        assert test == "test"
        return True

    job = Job(test="test")

    test_func.undo(job)


def test_no_undo_operation_decorator_job_attribute():

    job = Job(test="test")

    @no_undo_operation()
    def test_func(test, job):
        assert test == "test"
        assert isinstance(job, Job)
        assert job == job
        return True

    test_func.do(job)


def test_no_do_operation_decorator_job_attribute():

    job = Job(test="test")

    @no_do_operation()
    def test_func(test, job):
        assert test == "test"
        assert isinstance(job, Job)
        assert job == job
        return True

    test_func.undo(job)


def test_no_undo_operation_decorator_retry():

    job = Job(counter=0)
    @no_undo_operation(3)
    def test_func(job):
        job.counter += 1
        if job.counter < 3:
            return False
        return True

    test_func.do(job)

    assert job.counter == 3
    assert not job.failure


def test_no_undo_operation_decorator_retry_failure():
    job = Job(counter=0)

    @no_undo_operation(2)
    def test_func(job):
        job.counter += 1
        return False

    test_func.do(job)

    assert job.counter == 3


def test_no_undo_operation_decorator_no_retry():
    job = Job(counter=0)

    @no_undo_operation()
    def test_func(job):
        job.counter += 1
        return False

    test_func.do(job)

    assert job.counter == 1

