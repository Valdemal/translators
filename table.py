from lexical import PredicateTransfer, ValueTransfer, ManyValuesTransfer, Lexeme

TABLE = [
    [
        PredicateTransfer(str.isspace, 0),
        ValueTransfer('a', 2),
        ValueTransfer('o', 5),
        ValueTransfer('x', 6),
        ValueTransfer('n', 8),
        ValueTransfer('v', 10),
        ValueTransfer('b', 13),
        ValueTransfer('e', 17),
        ValueTransfer('r', 19),
        ValueTransfer('w', 22),
        ValueTransfer('t', 26),
        ValueTransfer('f', 27),
        ValueTransfer('s', 29),
        ValueTransfer(':', 32),
        ManyValuesTransfer(['+', '-', '*', '(', ')', ','], 33),
        PredicateTransfer(lambda char: char in '123456789', 34),
        ValueTransfer('/', 35),
        PredicateTransfer(str.isalnum, 1)
    ],  # s0
    [PredicateTransfer(str.isalnum, 1)],  # s1
    [ValueTransfer('n', 3), PredicateTransfer(str.isalnum, 1)],  # s2
    [ValueTransfer('d', 4), PredicateTransfer(str.isalnum, 1)],  # s3
    [PredicateTransfer(str.isalnum, 1)],  # s4
    [ValueTransfer('r', 4), PredicateTransfer(str.isalnum, 1)],  # s5
    [ValueTransfer('o', 7), PredicateTransfer(str.isalnum, 1)],  # s6
    [ValueTransfer('r', 4), PredicateTransfer(str.isalnum, 1)],  # s7
    [ValueTransfer('o', 9), PredicateTransfer(str.isalnum, 1)],  # s8
    [ValueTransfer('t', 4), PredicateTransfer(str.isalnum, 1)],  # s9
    [ValueTransfer('a', 11), PredicateTransfer(str.isalnum, 1)],  # s10
    [ValueTransfer('r', 12), PredicateTransfer(str.isalnum, 1)],  # s11
    [PredicateTransfer(str.isalnum, 1)],  # s12
    [ValueTransfer('e', 14), PredicateTransfer(str.isalnum, 1)],  # s13
    [ValueTransfer('g', 15), PredicateTransfer(str.isalnum, 1)],  # s14
    [ValueTransfer('i', 16), PredicateTransfer(str.isalnum, 1)],  # s15
    [ValueTransfer('n', 12), PredicateTransfer(str.isalnum, 1)],  # s16
    [ValueTransfer('e', 18), PredicateTransfer(str.isalnum, 1)],  # s17
    [ValueTransfer('d', 12), PredicateTransfer(str.isalnum, 1)],  # s18
    [ValueTransfer('e', 20), PredicateTransfer(str.isalnum, 1)],  # s19
    [ValueTransfer('a', 21), PredicateTransfer(str.isalnum, 1)],  # s20
    [ValueTransfer('d', 12), PredicateTransfer(str.isalnum, 1)],  # s21
    [ValueTransfer('r', 23), PredicateTransfer(str.isalnum, 1)],  # s22
    [ValueTransfer('i', 24), PredicateTransfer(str.isalnum, 1)],  # s23
    [ValueTransfer('t', 25), PredicateTransfer(str.isalnum, 1)],  # s24
    [ValueTransfer('e', 12), PredicateTransfer(str.isalnum, 1)],  # s25
    [ValueTransfer('o', 12), PredicateTransfer(str.isalnum, 1)],  # s26
    [ValueTransfer('o', 28), PredicateTransfer(str.isalnum, 1)],  # s27
    [ValueTransfer('r', 12), PredicateTransfer(str.isalnum, 1)],  # s28
    [ValueTransfer('t', 30), PredicateTransfer(str.isalnum, 1)],  # s29
    [ValueTransfer('e', 31), PredicateTransfer(str.isalnum, 1)],  # s30
    [ValueTransfer('p', 12), PredicateTransfer(str.isalnum, 1)],  # s31
    [ValueTransfer('=', 33)],  # s32
    [],  # s33 разрешающее состояние
    [PredicateTransfer(str.isdigit, 34)],  # s34 разрешающее состояние
    [ValueTransfer('*', 36)],  # s35 разрешающее состояние
    [PredicateTransfer(lambda char: char != '*', 36), ValueTransfer('*', 37)],  # s36
    [ValueTransfer('/', 0)],  # s37
    [],  # s38 разрешающее состояние
]

RESOLVE_STATES = [1, 4, 12, 33, 34, 35, 38]


def lexeme_factory(state: int, value: str) -> Lexeme:
    if state == 1:
        return Lexeme(value, Lexeme.Type.IDENTIFIER)
    elif state == 34:
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
