from dataclasses import dataclass


@dataclass
class Job:
    failure: bool = False

    def __init__(self, base_attributes: dict = None, **kwargs):
        if base_attributes:
            for key, value in base_attributes.items():
                self.__setattr__(key, value)
        for key, value in kwargs.items():
            self.__setattr__(key, value)
