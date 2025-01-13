from abc import ABC

from .text_wrapper import TextWrapper


class Transfer(ABC):
    def __init__(self, target_state_index: int):
        self.target_state = target_state_index

    def __call__(self, text_wrapper: TextWrapper):
        text_wrapper.state_index = self.target_state
        text_wrapper.next()


class SkipTransfer(Transfer):
    def __call__(self, text_wrapper: TextWrapper):
        text_wrapper.state_index = self.target_state
        text_wrapper.skip()


class HoldTransfer(Transfer):
    def __call__(self, text_wrapper: TextWrapper):
        text_wrapper.state_index = self.target_state


class DropTransfer(Transfer):
    def __call__(self, text_wrapper: TextWrapper):
        text_wrapper.state_index = self.target_state
        text_wrapper.next()
        text_wrapper.drop_buffer()
