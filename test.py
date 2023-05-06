import asyncio

from tgbot import config
from tgbot.db.db_api import get_industries
import pprint
from tgbot.config import load_config


async def main():
    print('hello')
    config = load_config()
    resp = await get_industries(config, lang="ru", parent_str=1)
    pprint.pprint(resp)
    asyncio.run(main())
