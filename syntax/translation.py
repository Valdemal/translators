from abc import abstractmethod, ABC

from lexical.analyzer import Lexeme
from syntax.store import Store


class Translation(ABC):
    def __add__(self, other) -> 'Translation':
        return TranslationComposite(self, other)

    @abstractmethod
    def __call__(self, store: Store):
        pass


class TranslationComposite(Translation):
    def __init__(self, *translations):
        self._translations = translations

    def __call__(self, store: Store):
        for translation in self._translations:
            translation(store)


class ValueTranslation(Translation):
    def __init__(self, value: str):
        self._value = value

    def __call__(self, store: Store):
        store.append(self._value)


class LexemeTranslation(Translation):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(store.peek().value)
        else:
            print("Кажись ошибка")


class ReadTranslation(Translation):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(f'printf("i = "); scanf(&{store.peek().value});')
        else:
            print("Кажись ошибка")


class WriteTranslation(Translation):
    def __call__(self, store: Store):
        if isinstance(store.peek(), Lexeme):
            store.append(f'printf("i = %d\n", {store.peek().value});')
        else:
            print("Кажись ошибка")
