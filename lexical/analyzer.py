from dataclasses import dataclass
from enum import Enum, auto

from lexical.state import State
from lexical.text_wrapper import TextWrapper


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
        OPENING_BRACKET = auto()
        CLOSING_BRACKET = auto()
        COMMA = auto()

    value: str
    type: Type


class LexicalAnalysisError(Exception):
    pass


class LexicalAnalyzer:
    def __init__(self, table: list[State], lexeme_factory):
        self._table = table
        self._lexeme_factory = lexeme_factory
        self._lexemes = []

    @property
    def lexemes(self):
        return self._lexemes

    def analyze(self, text: str):
        text_wrapper = TextWrapper(text)

        while not text_wrapper.end():
            state = self._table[text_wrapper.state_index]
            transfer = state.get_transfer(text_wrapper.char)

            if transfer:
                transfer(text_wrapper)
            elif state.is_permissive:
                self._lexemes.append(self._lexeme_factory(text_wrapper.state_index, text_wrapper.buffer))
                text_wrapper.state_index = 0
                text_wrapper.drop_buffer()
            else:
                raise LexicalAnalysisError(f"Ошибка при лексическом анализе. Символ {text_wrapper.char}. Состояние {text_wrapper.state_index}")

        state = self._table[text_wrapper.state_index]
        if not state.is_permissive:
            raise LexicalAnalysisError(f"Ошибка при лексическом анализе. Символ {text_wrapper.char}. Состояние {text_wrapper.state_index}")
