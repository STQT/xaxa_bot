import typing

from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class BackFilter(BoundFilter):

    def __init__(self, is_back: typing.Optional[bool] = None):
        self.is_back = is_back

    async def check(self, m: Message):
        if m.text == '🔙 Orqaga':
            return False
        return True
