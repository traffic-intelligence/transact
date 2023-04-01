from dataclasses import dataclass


@dataclass
class Job:
    failure: bool = False
    attr_list: list[str] = None

    def __init__(self, base_attributes: dict = None, **kwargs):
        self.attr_list = ["failure"]

        if base_attributes:
            for key, value in base_attributes.items():
                self.__setattr__(key, value)
                self.attr_list.append(key)
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            self.attr_list.append(key)

    def __eq__(self, other):

        if isinstance(other, Job):
            if len(other.attr_list) != len(self.attr_list):
                return False
            if not all([a == b for a, b in zip(other.attr_list, self.attr_list)]):
                return False
            if not all([other.__getattribute__(a) == self.__getattribute__(b) for a, b in
                        zip(other.attr_list, self.attr_list)]):
                return False
            return True

        return False
