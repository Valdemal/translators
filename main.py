from config import TABLE, lexeme_factory
from lexical.analyzer import LexicalAnalyzer

if __name__ == '__main__':
    text = "BEGIN VAR aa := bbb123n +nnb /*комментарий*/ end - begin122 ag / + (,) * 123 not  and"
    analyzer = LexicalAnalyzer(TABLE, lexeme_factory)
    analyzer.analyze(text)

    print("Лексема".ljust(15), '|', "Тип лексемы".ljust(20))
    print('-' * 37)
    for lexeme in analyzer.lexemes:
        print(lexeme.value.ljust(15), '|', str(lexeme.type).ljust(20))