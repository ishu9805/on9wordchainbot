from pyrogram import types
from pyrogram.filters import Filter

from .constants import OWNER_ID, VIP
from .bot import bot  # Assuming you have a bot instance defined


class OwnerFilter(Filter):
    def __init__(self):
        super().__init__(self.is_owner)

    async def is_owner(self, _, __, message: types.Message):
        return message.from_user.id == OWNER_ID


class VIPFilter(Filter):
    def __init__(self):
        super().__init__(self.is_vip)

    async def is_vip(self, _, __, message: types.Message):
        return message.from_user.id in VIP


class AdminFilter(Filter):
    async def check(self, _, __, message: types.Message):
        if message.from_user.id == OWNER_ID:
            return True
        chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return chat_member.status == "administrator"


class GameRunningFilter(Filter):
    async def check(self, _, __, message: types.Message):
        from . import GlobalState

        # Game running in chat implies chat is a group
        return (
            message.chat.type in ("group", "supergroup")
            and message.chat.id in GlobalState.games
        )


filters = [
    OwnerFilter(),
    VIPFilter(),
    AdminFilter(),
    GameRunningFilter()
]
