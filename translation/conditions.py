from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def __call__(self, char) -> bool:
        pass


class ValueCondition(Condition):
    def __init__(self, value):
        self._value = value

    def __call__(self, char) -> bool:
        return char == self._value


class ManyValuesCondition(Condition):
    def __init__(self, *values):
        self._values = values

    def __call__(self, char) -> bool:
        return char in self._values
