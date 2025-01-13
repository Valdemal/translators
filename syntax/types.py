from dataclasses import dataclass
from typing import Sequence

from lexical.analyzer import Lexeme

StackSymbol = Lexeme or str or 'Translation'


@dataclass
class Rule:
    left: str
    right: Sequence[Lexeme.Type or str] or None
