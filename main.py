from lexical import LexicalAnalyzer
from table import TABLE, RESOLVE_STATES

if __name__ == '__main__':
    text = "BEGIN VAR aa := bbb123n +nn END"
    analyzer = LexicalAnalyzer(TABLE, RESOLVE_STATES)
    analyzer.analyze(text)
    print(analyzer.lexemes)
