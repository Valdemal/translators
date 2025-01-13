from typing import List

from translation.types import StackSymbol


class Store:
    def __init__(self):
        self._index = 0
        self._output = ''
        self._stack: List[StackSymbol] = ['S']

    @property
    def is_empty(self) -> bool:
        return len(self._stack) == 0

    @property
    def index(self) -> int:
        return self._index

    @property
    def output(self) -> str:
        return self._output

    def append(self, s: str):
        self._output += s

    def shift(self):
        self._index += 1

    def peek(self) -> StackSymbol:
        return self._stack[-1]

    def pop(self):
        return self._stack.pop()

    def replace(self, symbols: List[StackSymbol]):
        self._stack.pop()
        self._stack += symbols

    def __str__(self):
        return f"""
        Index: {self._index};
        Output: {self._output};
        Stack:\n""" + "\n".join(map(str, reversed(self._stack)))
