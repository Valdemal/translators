from typing import List, Tuple

from lexical.analyzer import Lexeme
from lexical.conditions import ValueCondition, ManyValuesCondition
from lexical.state import State
from lexical.transfer import SkipTransfer, Transfer, DropTransfer, HoldTransfer
from syntax.types import Rule
from syntax.translation import ValueTranslation, LexemeTranslation, ReadTranslation, WriteTranslation

TABLE = [
    State(
        (str.isspace, SkipTransfer(0)),
        (ValueCondition('a'), Transfer(8)),
        (ValueCondition('n'), Transfer(11)),
        (ValueCondition('f'), Transfer(13)),
        (ValueCondition('s'), Transfer(15)),
        (ValueCondition('t'), Transfer(18)),
        (ValueCondition('w'), Transfer(19)),
        (ValueCondition('r'), Transfer(23)),
        (ValueCondition('e'), Transfer(26)),
        (ValueCondition('b'), Transfer(28)),
        (ValueCondition('v'), Transfer(32)),
        (ValueCondition('o'), Transfer(34)),
        (ValueCondition('x'), Transfer(35)),
        (str.isalpha, Transfer(1)),
        (lambda char: char in '123456789', Transfer(2)),
        (ValueCondition(':'), Transfer(3)),
        (ManyValuesCondition('+', '-', '*', '(', ')', ','), Transfer(4)),
        (ValueCondition('/'), Transfer(5)),
        (ValueCondition('˧'), Transfer(37))
    ),  # S0
    State((str.isalnum, Transfer(1)), is_permissive=True),  # S1
    State((str.isdigit, Transfer(2)), is_permissive=True),  # S2
    State((ValueCondition('='), Transfer(4))),  # S3
    State(is_permissive=True),  # S4
    State((ValueCondition('*'), Transfer(6)), is_permissive=True),  # S5
    State((lambda char: char != '*', Transfer(6)), (ValueCondition('*'), Transfer(7))),  # S6
    State((ValueCondition('/'), DropTransfer(0))),  # S7
    State((ValueCondition('n'), Transfer(9)), default=HoldTransfer(1)),  # S8
    State((ValueCondition('d'), Transfer(10)), default=HoldTransfer(1)),  # S9
    State((str.isalnum, Transfer(1)), is_permissive=True),  # S10
    State((ValueCondition('o'), Transfer(12)), default=HoldTransfer(1)),  # S11
    State((ValueCondition('t'), Transfer(10)), default=HoldTransfer(1)),  # S12
    State((ValueCondition('o'), Transfer(14)), default=HoldTransfer(1)),  # S13
    State((ValueCondition('r'), Transfer(10)), default=HoldTransfer(1)),  # S14
    State((ValueCondition('t'), Transfer(16)), default=HoldTransfer(1)),  # S15
    State((ValueCondition('e'), Transfer(17)), default=HoldTransfer(1)),  # S16
    State((ValueCondition('p'), Transfer(10)), default=HoldTransfer(1)),  # S17
    State((ValueCondition('o'), Transfer(10)), default=HoldTransfer(1)),  # S18
    State((ValueCondition('r'), Transfer(20)), default=HoldTransfer(1)),  # S19
    State((ValueCondition('i'), Transfer(21)), default=HoldTransfer(1)),  # S20
    State((ValueCondition('t'), Transfer(22)), default=HoldTransfer(1)),  # S21
    State((ValueCondition('e'), Transfer(10)), default=HoldTransfer(1)),  # S22
    State((ValueCondition('e'), Transfer(24)), default=HoldTransfer(1)),  # S23
    State((ValueCondition('a'), Transfer(25)), default=HoldTransfer(1)),  # S24
    State((ValueCondition('d'), Transfer(10)), default=HoldTransfer(1)),  # S25
    State((ValueCondition('n'), Transfer(27)), default=HoldTransfer(1)),  # S26
    State((ValueCondition('d'), Transfer(10)), default=HoldTransfer(1)),  # S27
    State((ValueCondition('e'), Transfer(29)), default=HoldTransfer(1)),  # S28
    State((ValueCondition('g'), Transfer(30)), default=HoldTransfer(1)),  # S29
    State((ValueCondition('i'), Transfer(31)), default=HoldTransfer(1)),  # S30
    State((ValueCondition('n'), Transfer(10)), default=HoldTransfer(1)),  # S31
    State((ValueCondition('a'), Transfer(33)), default=HoldTransfer(1)),  # S32
    State((ValueCondition('r'), Transfer(10)), default=HoldTransfer(1)),  # S33
    State((ValueCondition('r'), Transfer(10)), default=HoldTransfer(1)),  # S34
    State((ValueCondition('o'), Transfer(36)), default=HoldTransfer(1)),  # S35
    State((ValueCondition('r'), Transfer(10)), default=HoldTransfer(1)),  # S36
    State(is_permissive=True),  # S37
]


def lexeme_factory(state: int, value: str) -> Lexeme:
    if state == 1:
        return Lexeme(value, Lexeme.Type.IDENTIFIER)
    elif state == 2:
        return Lexeme(value, Lexeme.Type.NUMBER)
    else:
        return Lexeme(value, {
            'or': Lexeme.Type.ADDITIVE, 'xor': Lexeme.Type.ADDITIVE,
            'and': Lexeme.Type.MULTIPLICATIVE, 'not': Lexeme.Type.NOT,
            'var': Lexeme.Type.VAR, 'begin': Lexeme.Type.BEGIN, 'end': Lexeme.Type.END,
            'read': Lexeme.Type.READ, 'write': Lexeme.Type.WRITE, 'for': Lexeme.Type.FOR,
            'to': Lexeme.Type.TO, 'step': Lexeme.Type.STEP, ':=': Lexeme.Type.ASSIGMENT,
            '+': Lexeme.Type.ADDITIVE, '-': Lexeme.Type.ADDITIVE, '*': Lexeme.Type.MULTIPLICATIVE,
            '/': Lexeme.Type.MULTIPLICATIVE, '(': Lexeme.Type.OPENING_BRACKET, ')': Lexeme.Type.CLOSING_BRACKET,
            ',': Lexeme.Type.COMMA
        }[value])


rules_to_choices: List[Tuple[Rule, List[Lexeme.Type]]] = [
    (
        Rule('S', [Lexeme.Type.VAR, ValueTranslation('int '), 'V', Lexeme.Type.BEGIN, ValueTranslation(';'), 'B']),
        [Lexeme.Type.VAR]
    ),
    (Rule('V', [Lexeme.Type.IDENTIFIER, LexemeTranslation(), 'I']), [Lexeme.Type.IDENTIFIER]),
    (Rule('I', [Lexeme.Type.IDENTIFIER, LexemeTranslation() + ValueTranslation(','), 'I']), [Lexeme.Type.IDENTIFIER]),
    (Rule('I', None), [Lexeme.Type.BEGIN]),
    (Rule('B', ['O', 'C']), [Lexeme.Type.READ, Lexeme.Type.WRITE, Lexeme.Type.IDENTIFIER, Lexeme.Type.FOR]),
    (Rule('C', ['B']), [Lexeme.Type.READ, Lexeme.Type.WRITE, Lexeme.Type.IDENTIFIER, Lexeme.Type.FOR]),
    (Rule('C', None), [Lexeme.Type.END_OF_PROGRAM, Lexeme.Type.END]),
    (Rule('O', [Lexeme.Type.READ, Lexeme.Type.OPENING_BRACKET, 'R', Lexeme.Type.CLOSING_BRACKET]), [Lexeme.Type.READ]),
    (
        Rule('O', [Lexeme.Type.WRITE, Lexeme.Type.OPENING_BRACKET, 'W', Lexeme.Type.CLOSING_BRACKET]),
        [Lexeme.Type.WRITE]
    ),
    (Rule('O', [Lexeme.Type.IDENTIFIER, LexemeTranslation(), Lexeme.Type.ASSIGMENT, 'E']), [Lexeme.Type.IDENTIFIER]),
    (Rule('O', [Lexeme.Type]), [Lexeme.Type.FOR]),  # todo доделать цикл
    (Rule('R', [Lexeme.Type.IDENTIFIER, ReadTranslation(), 'R']), [Lexeme.Type.IDENTIFIER]),
    (Rule('R', None), [Lexeme.Type.CLOSING_BRACKET]),
    (Rule('W', [Lexeme.Type.IDENTIFIER, WriteTranslation(), 'W']), [Lexeme.Type.IDENTIFIER]),
    (Rule('W', None), [Lexeme.Type.CLOSING_BRACKET]),
    (Rule('E', ['T', 'F']), [Lexeme.Type.IDENTIFIER, Lexeme.Type.NUMBER, Lexeme.Type.NOT]),
    (Rule('F', [Lexeme.Type.ASSIGMENT, LexemeTranslation(), 'T', 'F']), [Lexeme.Type.ASSIGMENT]),
    (Rule('F', None), [Lexeme.Type.END_OF_PROGRAM, Lexeme.Type.END, Lexeme.Type.TO, Lexeme.Type.CLOSING_BRACKET]),
    (Rule('T', ['M', 'Q']), [Lexeme.Type.IDENTIFIER, Lexeme.Type.NUMBER, Lexeme.Type.NOT]),
    (Rule('Q', [Lexeme.Type.MULTIPLICATIVE, LexemeTranslation(), 'M', 'Q']), [Lexeme.Type.MULTIPLICATIVE]),
    (Rule('Q', None), [Lexeme.Type.END_OF_PROGRAM, Lexeme.Type.END, Lexeme.Type.TO, Lexeme.Type.CLOSING_BRACKET]),
    (Rule('M', [Lexeme.Type.IDENTIFIER, LexemeTranslation()]), [Lexeme.Type.IDENTIFIER]),
    (Rule('M', [Lexeme.Type.NUMBER]), [Lexeme.Type.NUMBER]),
    (Rule('M', [Lexeme.Type.NOT, LexemeTranslation(), Lexeme.Type.OPENING_BRACKET, LexemeTranslation(), 'E',
                Lexeme.Type.CLOSING_BRACKET, LexemeTranslation()]), [Lexeme.Type.NOT]),
]
