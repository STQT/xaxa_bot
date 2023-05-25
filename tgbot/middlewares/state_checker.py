from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.handlers.register import user_start


class MainMenuRedirectMiddleware(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, result: dict, config):
        # Send "Hello, world!" as a reply to any handler response
        state = await config['state'].get_state()
        if state is None:
            await user_start(message, config['status'], config['config'])
