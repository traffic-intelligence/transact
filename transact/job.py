from dataclasses import dataclass


@dataclass
class Job:
    failure: bool = False
