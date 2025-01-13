from typing import List, Tuple

from lexical.analyzer import Lexeme
from syntax.store import Store
from syntax.translation import Translation
from syntax.types import Rule, StackSymbol


class SyntaxAnalyzer:
    def __init__(self, rules_to_choices: List[Tuple[Rule, List[Lexeme.Type]]]):
        self._table = {}
        for rule, choices_set in rules_to_choices:
            operation = self.__make_operation(rule.right)
            self._table[rule.left] = {}
            for lexeme_type in choices_set:
                self._table[rule.left][lexeme_type] = operation

    def analyze(self, lexemes: list[Lexeme]) -> str:
        store = Store()

        while store.index < len(lexemes):
            top = store.peek()
            current = lexemes[store.index]

            if isinstance(top, Lexeme):
                if top.Type == current.Type:
                    store.pop()
                    store.shift()
                else:
                    raise Exception('Ошибка при синтаксическом анализе')

            elif isinstance(top, Translation):
                top(store)

            elif isinstance(top, str) and (operation := self._table[top].get(current.type)):
                operation(store)
            else:
                raise Exception('Синтаксическая ошибка на лексеме ' + str(current))

        if not store.is_empty:
            raise Exception('Ошибка')

        return store.output

    @staticmethod
    def __make_operation(symbols: List[StackSymbol] or None):

        if symbols is None:
            return Store.pop

        elif isinstance(symbols[0], Lexeme.Type):

            if len(symbols) >= 2 and isinstance(symbols[1], Translation):
                def lexeme_operation_with_transition(store):
                    symbols[1](store)
                    store.replace(symbols[:1:-1])

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
