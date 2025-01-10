class TextWrapper:

    def __init__(self, text: str):
        self._text = text
        self._index = 0
        self._buffer = ''
        self.state_index = 0

    @property
    def char(self) -> str:
        if self._index < len(self._text):
            return self._text[self._index].lower()

        return '˧'

    @property
    def buffer(self) -> str:
        return self._buffer

    def skip(self):
        if self._index <= len(self._text):
            self._index += 1

    def next(self):
        self._buffer += self.char
        self.skip()

    def end(self) -> bool:
        return self._index > len(self._text)

    def drop_buffer(self):
        self._buffer = ''
