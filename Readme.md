# Transact Package

The transact package is a native python package that allows to build transactional python processes.

In transactional programming, a transaction consists of several operations. As soon as one of the 
operation fails, all successful operations have to be rolled back. This is important for example
in payment processing.

## Getting Started

To get started with transact clone the git repo and install it:
```commandline
pip install .
```

## Tutorial

The main component of the transact package is the `Transaction`. The `Transaction` class executes
each operation one after the other. If an operation fails, the transaction rolls back all
the previously successfully executed operations.
The transaction can be initialized by giving it a list of operations, which are 
executed in the order of the list. Each operation is given the same instance
of the `Job` class. The operation can read and set attributes of the job as well as do any other
actions that can be implemented in python. The main purpose of the job attribute is to pass
information from one operation to the next, as well as to allow information storing in case of 
a rollback.
The usual operation consists of an `action` and a `undo_action`. The `action` is an atomic set
of code. The `undo_action` is the set of instructions that undo whatever was done by the `action`.
To create an operation we need to create two functions that return a boolean. The bool is one 
of the ways that the orchestrator detects whether the operation was successful or not
(the orchestrator also detects exceptions). 
```python
from transact.job import Job

def do(job: Job) -> bool:
    job.__setattr__("test", True)
    return True

def undo(job: Job) -> bool:
    job.__delattr__("test")
    return True
```
With the functions the instruction can be initialized:

```python
from transact.operation import Operation

operation = Operation(do, undo)
```
If you want the operation to automatically retry the action when it fails, the retry counter
can be set:

```python
from transact.operation import Operation

operation = Operation(do, undo, retry=2)
```
With the `operation` the orchestrator can be initialized:

```python
from transact.transaction import Transaction
from transact.logging_operation import DoLoggingOperation, LoggingType
from transact.job import Job

operations = [
    operation,
    DoLoggingOperation(LoggingType.DEBUG, "This is an example")
]
job = Job()

transaction = Transaction(operations)

success = transaction.enqueue(job)
```
If an operation fails, the orchestrator automatically rolls back all the operation.

## Developing

To run all unittests use:
```commandline
pytest tests/*
```