from pprint import pprint

from lexical import LexicalAnalyzer
from table import TABLE, RESOLVE_STATES, lexeme_factory

if __name__ == '__main__':
    # todo не может нормально разобрать строку
    # последняя лексема пропадает
    # буква a не обрабатывается (понятно почему)
    # сделать цикл с комментариями

    text = "BEGIN VAR aa:=bbb123n +nnb end - begin122 ag / + ( , ) * 123 "
    analyzer = LexicalAnalyzer(TABLE, RESOLVE_STATES, lexeme_factory)
    analyzer.analyze(text)
    pprint(analyzer.lexemes)
