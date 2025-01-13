from typing import List, Tuple

from translation.action import Action
from translation.exceptions import SyntaxAnalysisError
from translation.store import Store
from translation.types import Rule, Lexeme, StackSymbol


class SyntaxAnalyzer:
    def __init__(self, rules_to_choices: List[Tuple[Rule, List[Lexeme.Type]]]):
        self._table = {}
        for rule, choices_set in rules_to_choices:
            if self._table.get(rule.left) is None:
                self._table[rule.left] = {}

            operation = self.__make_operation(rule.right)
            self._table[rule.left] |= {lexeme_type: operation for lexeme_type in choices_set}

    def analyze(self, lexemes: list[Lexeme]) -> str:
        store = Store(lexemes)

        while not store.is_end:
            if store.current_lexeme.type == Lexeme.Type.END_OF_PROGRAM and store.stack_is_empty:
                return store.output

            top = store.peek()

            if isinstance(top, str) and (operation := self._table[top].get(store.current_lexeme.type)):
                operation(store)
            elif store.current_lexeme.compare(top):
                store.pop()
                store.shift()
            elif isinstance(top, Action):
                store.pop()
                top(store)
            else:
                raise SyntaxAnalysisError(store.current_lexeme, store)

    @staticmethod
    def __make_operation(symbols: List[StackSymbol] or None):

        if symbols is None:
            return Store.pop

        elif isinstance(symbols[0], Lexeme.Type):

            if len(symbols) >= 2 and isinstance(symbols[1], Action):
                def lexeme_operation_with_transition(store):
                    symbols[1](store)
                    store.replace(symbols[:1:-1])
                    store.shift()

                return lexeme_operation_with_transition
            else:
                def lexeme_operation(store):
                    store.replace(symbols[:0:-1])
                    store.shift()

                return lexeme_operation

        elif isinstance(symbols[0], str):
            def non_term_operation(store):
                store.replace(symbols[::-1])

            return non_term_operation
