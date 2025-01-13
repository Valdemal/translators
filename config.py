from lexical.analyzer import Lexeme
from lexical.conditions import ValueCondition, ManyValuesCondition
from lexical.state import State
from lexical.transfer import SkipTransfer, Transfer, DropTransfer, HoldTransfer

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
