from typing import Tuple, List

from lexical.conditions import Condition
from lexical.transfer import Transfer


class State:
    def __init__(self, *cases: List[Tuple[Condition, Transfer]], default: Transfer = None, is_permissive=False):
        self._cases = cases
        self._default = default
        self._is_permissive = is_permissive

    @property
    def is_permissive(self):
        return self._is_permissive

    def get_transfer(self, char) -> Transfer or None:
        for condition, transfer in self._cases:
            if condition(char):
                return transfer

        return self._default if self._default else None
