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
        (ValueCondition('˧'), Transfer(38))
    ),  # S0
    State((str.isalnum, Transfer(1)), is_permissive=True),  # S1
    State((str.isdigit, Transfer(2)), is_permissive=True),  # S2
    State((ValueCondition('='), Transfer(4))),  # S3
    State(is_permissive=True),  # S4 todo!!!
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
    State(is_permissive=True),  # S38
]


# TABLE = [
#     [
#         PredicateTransfer(str.isspace, 0),
#         ValueTransfer('a', 2),
#         ValueTransfer('o', 5),
#         ValueTransfer('x', 6),
#         ValueTransfer('n', 8),
#         ValueTransfer('v', 10),
#         ValueTransfer('b', 13),
#         ValueTransfer('e', 17),
#         ValueTransfer('r', 19),
#         ValueTransfer('w', 22),
#         ValueTransfer('t', 26),
#         ValueTransfer('f', 27),
#         ValueTransfer('s', 29),
#         ValueTransfer(':', 32),
#         ManyValuesTransfer(['+', '-', '*', '(', ')', ','], 33),
#         PredicateTransfer(lambda char: char in '123456789', 34),
#         ValueTransfer('/', 35),
#         PredicateTransfer(str.isalnum, 1)
#     ],  # s0
#     [PredicateTransfer(str.isalnum, 1)],  # s1
#     [ValueTransfer('n', 3), PredicateTransfer(str.isalnum, 1)],  # s2
#     [ValueTransfer('d', 4), PredicateTransfer(str.isalnum, 1)],  # s3
#     [PredicateTransfer(str.isalnum, 1)],  # s4
#     [ValueTransfer('r', 4), PredicateTransfer(str.isalnum, 1)],  # s5
#     [ValueTransfer('o', 7), PredicateTransfer(str.isalnum, 1)],  # s6
#     [ValueTransfer('r', 4), PredicateTransfer(str.isalnum, 1)],  # s7
#     [ValueTransfer('o', 9), PredicateTransfer(str.isalnum, 1)],  # s8
#     [ValueTransfer('t', 4), PredicateTransfer(str.isalnum, 1)],  # s9
#     [ValueTransfer('a', 11), PredicateTransfer(str.isalnum, 1)],  # s10
#     [ValueTransfer('r', 12), PredicateTransfer(str.isalnum, 1)],  # s11
#     [PredicateTransfer(str.isalnum, 1)],  # s12
#     [ValueTransfer('e', 14), PredicateTransfer(str.isalnum, 1)],  # s13
#     [ValueTransfer('g', 15), PredicateTransfer(str.isalnum, 1)],  # s14
#     [ValueTransfer('i', 16), PredicateTransfer(str.isalnum, 1)],  # s15
#     [ValueTransfer('n', 12), PredicateTransfer(str.isalnum, 1)],  # s16
#     [ValueTransfer('e', 18), PredicateTransfer(str.isalnum, 1)],  # s17
#     [ValueTransfer('d', 12), PredicateTransfer(str.isalnum, 1)],  # s18
#     [ValueTransfer('e', 20), PredicateTransfer(str.isalnum, 1)],  # s19
#     [ValueTransfer('a', 21), PredicateTransfer(str.isalnum, 1)],  # s20
#     [ValueTransfer('d', 12), PredicateTransfer(str.isalnum, 1)],  # s21
#     [ValueTransfer('r', 23), PredicateTransfer(str.isalnum, 1)],  # s22
#     [ValueTransfer('i', 24), PredicateTransfer(str.isalnum, 1)],  # s23
#     [ValueTransfer('t', 25), PredicateTransfer(str.isalnum, 1)],  # s24
#     [ValueTransfer('e', 12), PredicateTransfer(str.isalnum, 1)],  # s25
#     [ValueTransfer('o', 12), PredicateTransfer(str.isalnum, 1)],  # s26
#     [ValueTransfer('o', 28), PredicateTransfer(str.isalnum, 1)],  # s27
#     [ValueTransfer('r', 12), PredicateTransfer(str.isalnum, 1)],  # s28
#     [ValueTransfer('t', 30), PredicateTransfer(str.isalnum, 1)],  # s29
#     [ValueTransfer('e', 31), PredicateTransfer(str.isalnum, 1)],  # s30
#     [ValueTransfer('p', 12), PredicateTransfer(str.isalnum, 1)],  # s31
#     [ValueTransfer('=', 33)],  # s32
#     [],  # s33 разрешающее состояние
#     [PredicateTransfer(str.isdigit, 34)],  # s34 разрешающее состояние
#     [ValueTransfer('*', 36)],  # s35 разрешающее состояние
#     [PredicateTransfer(lambda char: char != '*', 36), ValueTransfer('*', 37)],  # s36
#     [ValueTransfer('/', 0)],  # s37
#     [],  # s38 разрешающее состояние
# ]


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
            '/': Lexeme.Type.MULTIPLICATIVE, '(': Lexeme.Type.SPECIAL, ')': Lexeme.Type.SPECIAL,
            ',': Lexeme.Type.SPECIAL
        }[value])
