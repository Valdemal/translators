from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable, List


@dataclass
class Lexeme:
    class Type(Enum):
        IDENTIFIER = auto()
        NUMBER = auto()
        VAR = auto()
        BEGIN = auto()
        END = auto()
        READ = auto()
        WRITE = auto()
        FOR = auto()
        TO = auto()
        STEP = auto()
        NOT = auto()
        ADDITIVE = auto()
        MULTIPLICATIVE = auto()
        ASSIGMENT = auto()
        SPECIAL = auto()

    value: str
    type: Type


class Transfer:
    def __init__(self, target_state: int, default_state: int = None):
        self.target_state = target_state
        self.default_state = default_state

    @abstractmethod
    def __call__(self, char) -> bool:
        pass


class ValueTransfer(Transfer):
    def __init__(self, target_value, target_state, default_state=None):
        super().__init__(target_state, default_state)
        self.target_value = target_value

    def __call__(self, char) -> bool:
        return char == self.target_value


class ManyValuesTransfer(Transfer):
    def __init__(self, target_values: Iterable, target_state, default_state=None):
        super().__init__(target_state, default_state)
        self.target_values = target_values

    def __call__(self, char) -> bool:
        return char in self.target_values


class PredicateTransfer(Transfer):
    def __init__(self, target_predicate: Callable[[str], bool], target_state, default_state=None):
        super().__init__(target_state, default_state)
        self.target_predicate = target_predicate

    def __call__(self, char):
        return self.target_predicate(char)


class LexicalAnalysisError(Exception):
    pass


class LexicalAnalyzer:
    def __init__(self, table: List[List[Transfer]], resolve_states: List[int],
                 lexeme_factory: Callable[[int, str], Lexeme]):
        self._table = table
        self._resolve_states = resolve_states
        self._lexeme_factory = lexeme_factory
        self._lexemes = []

    @property
    def lexemes(self):
        return self._lexemes

    def analyze(self, text: str):
        state = 0
        buffer = ''
        i = 0

        while i < len(text):
            char = text[i].lower()
            new_state = self._get_next_state(char, state)

            if new_state is not None:
                # переход в новое состояние
                state = new_state
                if not char.isspace():  # todo Костыль
                    buffer += char
                i += 1
            else:
                if state in self._resolve_states:
                    self._lexemes.append(self._lexeme_factory(state, buffer))
                    state = 0
                    buffer = ''
                else:
                    print(state, char)
                    raise LexicalAnalysisError('Ошибка при лексическом анализе')

    def _get_next_state(self, char, old_state) -> int or None:
        new_state = None  # по умолчанию новое состояние - состояние ошибки

        for transfer in self._table[old_state]:
            if transfer(char):
                new_state = transfer.target_state
                break

        return new_state
