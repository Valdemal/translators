from abc import abstractmethod, ABC

from translation.store import Store
from translation.types import Lexeme


class Action(ABC):
    def __add__(self, other) -> 'Action':
        return ActionComposite(self, other)

    @abstractmethod
    def __call__(self, store: Store):
        pass


class ActionComposite(Action):
    def __init__(self, *translations):
        self._translations = translations

    def __call__(self, store: Store):
        for translation in self._translations:
            translation(store)


class ValueAction(Action):
    def __init__(self, value: str):
        self._value = value

    def __call__(self, store: Store):
        store.append(self._value)


class LexemeAction(Action):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(store.peek().value)
        else:
            print("Кажись ошибка")


class ReadAction(Action):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(f'printf("i = "); scanf(&{store.peek().value});')
        else:
            print("Кажись ошибка")


class WriteAction(Action):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(f'printf("i = %d\n", {store.peek().value});')
        else:
            print("Кажись ошибка")
