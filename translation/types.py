from dataclasses import dataclass
from enum import Enum, auto
from typing import Sequence


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
        END_OF_PROGRAM = auto()

    value: str
    type: Type

    def compare(self, other: 'Lexeme' or 'Lexeme.Type') -> bool:
        if isinstance(other, Lexeme.Type):
            return self.type == other
        elif isinstance(other, Lexeme):
            return self.type == other.type


StackSymbol = Lexeme or str or 'Translation'


@dataclass
class Rule:
    left: str
    right: Sequence[Lexeme.Type or str] or None
