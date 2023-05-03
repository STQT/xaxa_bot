from typing import List

from tgbot.db.models import *


async def create_user(tg_id, lang, name, number, us_type, region, product=None) -> User:
    return await User.create(tg_id=tg_id, lang=lang, name=name, number=number, type=us_type, status="basic",
                             region=region, product=product)


async def update_user(tg_id, status) -> None:
    user = await User.query.where(User.tg_id == tg_id).gino.first()
    await user.update(status=status).apply()


async def get_count(region, type) -> None:
    res = await User.query.count(User.region == region | User.type == type).gino.first()
    print(res)

async def get_user(tg_id) -> User:
    return await User.query.where(User.tg_id == tg_id).gino.first()


async def get_cities() -> List[City]:
    return await City.query.gino.all()


async def get_markets(address) -> List[Market]:
    return await Market.query.where(Market.address.ilike(f"%{address}%")).gino.all()


async def get_market_id(market_id) -> Market:
    return await Market.query.where(Market.id == int(market_id)).gino.first()


async def get_quarters(city) -> List[Quarter]:
    return await Quarter.query.where(Quarter.name == city).gino.all()
