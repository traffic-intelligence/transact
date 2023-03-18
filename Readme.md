# Transact Package

The transact package is a native python package that allows to build transactional python processes.

## Getting Started

To get started with transact clone the git repo and install it:
```commandline
pip install .
```

## Tutorial

The main component of the transact package is the `Orchestrator`. The `Orchestrator` executes
each transaction one after the other. If a transaction fails, the orchestrator rolls back all
the previously successfully executed transactions.
The orchestrator can be initialized by giving it a list of transactions. The orchestrator 
executes these transactions in the order of the list. Each transaction is given the same instance
of the `Job` class. The transaction can read and set attributes of the job as well as do any other
actions that can be implemented in python.
The usual transaction consists of an `action` and a `undo_action`. The `action` is an atomic set
of code. The `undo_action` is the set of instructions that undo whatever was done by the `action`.
To create a transaction we need to create two functions that return a boolean. The bool is one 
of the ways that the orchestrator detects whether the transaction was successful or not
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
from transact.transaction import Transaction

transaction = Transaction(do, undo)
```
If you want the transaction to automatically retry the action when it fails, the retry counter
can be set:
```python
from transact.transaction import Transaction

transaction = Transaction(do, undo, retry=2)
```
With the `transaction` the orchestrator can be initialized:
```python
from transact.orchestrator import Orchestrator
from transact.logging_transaction import DoLoggingTransaction, LoggingType
from transact.job import Job

transactions = [
    transaction,
    DoLoggingTransaction(LoggingType.DEBUG, "This is an example")
]
job = Job()

orchestrator = Orchestrator(transactions)

success = orchestrator.enqueue(job)
```
If a transaction fails, the orchestrator automatically rolls back all the transaction.

