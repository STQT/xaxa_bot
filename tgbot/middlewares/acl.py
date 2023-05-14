from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.db_api import get_user


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User):
        # data["user"] = "uz"
        # data["user_lang"] = "uz"
        # data['status'] = False
        # data['lang'] = "uz"
        # data["user_type"] = "distributor"
        user_loc = await get_user(user.id, data['config'])
        if "detail" in user_loc:
            data['user_lang'], data['status'] = user.language_code, True
        else:
            data['user_lang'], data['status'] = user_loc["lang"], False
            data['user'] = user_loc

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
