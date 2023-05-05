from typing import List

import aiohttp


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}users/{user_id}") as response:
            return await response.json()


async def create_user(tg_id, name, user_lang, user_phone, user_type, region, config):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": "Token 4ffe410d52f954ad113011c2a64cd3b3aace4ba3"}
        async with session.post(headers=headers,
                                url=f"{config.db.database_url}create-user/",
                                json={"tg_id": tg_id, "tg_name": name, "lang": user_lang, "phone": user_phone,
                                      "user_type": user_type,
                                      "region": region}) as response:
            if response.status == 201:
                return await response.json()
            return False


async def pre_register_user(tg_id, region="dwd", category="fe", sub_category, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}users",
                                data={"tg_id": tg_id, "lang": user_lang, "phone": user_phone, "user_type": user_type})\
                as response:
            return await response.json()


async def get_industries(config) -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}categories") as response:
            return await response.json()


async def update_user(user_id, config, lang=False, phone=False, name=False):
    data = {}
    if phone:
        data["user_phone"] = phone
    if lang:
        data["user_lang"] = lang
    if name:
        data["user_name"] = name
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"{config.db.database_url}user/update/{user_id}",
                                 data=data) as response:
            return await response.json()


async def get_contacts(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}calls/") as response:
            return await response.json()


async def get_prod_cats(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}category/") as response:
            return await response.json()


async def get_prods(filter_type, option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/", params={"filter_type": filter_type,
                                                                                       "option": option}) as response:
            return await response.json()


async def update_cart(user_id, option, config, obj_id=None, quan=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}cart/update", data={"tg_id": user_id,
                                                                                         "option": option,
                                                                                         "id": obj_id,
                                                                                         "quan": quan}) as response:
            return await response.json()


async def get_cart(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}cart/{user_id}") as response:
            return await response.json()
