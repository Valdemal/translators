from config import TABLE, lexeme_factory, rules_to_choices
from translation import LexicalAnalyzer, SyntaxAnalyzer

if __name__ == '__main__':
    # text = "BEGIN VAR aa := bbb123n +nnb /*комментарий*/ end - begin122 ag / + (,) * 123 not  and"
    text = "VAR i, c BEGIN c := 2"
    lexical_analyzer = LexicalAnalyzer(TABLE, lexeme_factory)
    lexemes = lexical_analyzer.analyze(text)

    print("Лексема".ljust(15), '|', "Тип лексемы".ljust(20))
    print('-' * 37)
    for lexeme in lexemes:
        print(lexeme.value.ljust(15), '|', str(lexeme.type).ljust(20))

    syntax_analyzer = SyntaxAnalyzer(rules_to_choices)

    syntax_analyzer.analyze(lexemes)
