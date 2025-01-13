from abc import abstractmethod, ABC

from translation.store import Store


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
        store.append(store.current_lexeme.value)


class ReadAction(Action):
    def __call__(self, store: Store):
        store.append(f'printf("{store.current_lexeme.value} = "); scanf("%d", &{store.current_lexeme.value});\n\t')


class WriteAction(Action):
    def __call__(self, store: Store):
        store.append(f'printf("{store.current_lexeme.value} = %d\\n", {store.current_lexeme.value});\n\t')
