from translation.store import Store
from translation.types import Lexeme


class TranslatorError(Exception):
    pass


class LexicalAnalysisError(TranslatorError):
    def __init__(self, char: str, state_index: int):
        super().__init__(f"Ошибка при лексическом анализе. Символ {char}. Состояние {state_index}")


class SyntaxAnalysisError(TranslatorError):
    def __init__(self, current_lexeme: Lexeme, store: Store):
        self.current_lexeme = Lexeme
        self.store = store
        super().__init__(f"Ошибка при синтаксическом анализе. Лексема: {str(current_lexeme)}.\n" + str(store))
