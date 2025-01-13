from translation.exceptions import LexicalAnalysisError
from translation.state import State
from translation.text_wrapper import TextWrapper
from translation.types import Lexeme


class LexicalAnalyzer:
    def __init__(self, table: list[State], lexeme_factory):
        self._table = table
        self._lexeme_factory = lexeme_factory

    def analyze(self, text: str) -> list[Lexeme]:
        lexemes: list[Lexeme] = []
        text_wrapper = TextWrapper(text)

        while not text_wrapper.end():
            state = self._table[text_wrapper.state_index]
            transfer = state.get_transfer(text_wrapper.char)

            if transfer:
                transfer(text_wrapper)
            elif state.is_permissive:
                lexemes.append(self._lexeme_factory(text_wrapper.state_index, text_wrapper.buffer))
                text_wrapper.state_index = 0
                text_wrapper.drop_buffer()
            else:
                raise LexicalAnalysisError(text_wrapper.char, text_wrapper.state_index)

        state = self._table[text_wrapper.state_index]
        if not state.is_permissive:
            raise LexicalAnalysisError(text_wrapper.char, text_wrapper.state_index)

        lexemes.append(Lexeme('┤', Lexeme.Type.END_OF_PROGRAM))

        return lexemes
