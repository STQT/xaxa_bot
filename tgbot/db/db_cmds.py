from typing import List

from tgbot.db.models import User, City, Market


async def create_user(tg_id, lang) -> User:
    print(lang)
    new_user = await User.create(tg_id=tg_id, lang=str(lang))
    return new_user


async def get_user(tg_id) -> User:
    new_user = await User.query.where(User.tg_id == tg_id).gino.first()
    return new_user


async def get_cities() -> List[City]:
    return await City.query.gino.all()


async def get_markets(address, region) -> List[Market]:
    return await Market.query.where(Market.address.like(f"%{address}%")).gino.all()


async def get_market_id(market_id) -> Market:
    return await Market.query.where(Market.id == int(market_id)).gino.first()

