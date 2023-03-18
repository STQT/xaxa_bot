import aiohttp


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}user/update/{user_id}") as response:
            return await response.json()


async def create_user(user_id, user_lang, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}user/create/",
                                data={"tg_id": user_id, "user_lang": user_lang}) as response:
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
