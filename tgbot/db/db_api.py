import urllib.parse
from typing import List

import aiohttp


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}users/{user_id}") as response:
            return await response.json()


async def check_user(user_id, user_type, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}{user_type}/{user_id}/") as response:
            if response.status == 200:
                return True
            return False


async def create_user(tg_id, name, user_lang, user_phone, user_type, region, config):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": "Token 4ffe410d52f954ad113011c2a64cd3b3aace4ba3"}
        url = f"{config.db.database_url}create-user/"
        async with session.post(headers=headers,
                                url=url,
                                json={"tg_id": tg_id, "tg_name": name, "lang": user_lang, "phone": user_phone,
                                      "user_type": user_type,
                                      "region": region}) as response:
            if response.status == 201:
                return await response.json()
            return False


async def pre_register_user(config, user_type: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}{user_type}/", data=data) as response:
            print(response.text)
            if response.status == 201:
                return await response.json()
            else:
                raise ConnectionError


async def get_industries(config, lang: str, parent_str: str = None) -> List:
    async with aiohttp.ClientSession() as session:
        fetch_url = config.db.database_url + f"categories/?lang={lang}&parent_str="
        parent_str = urllib.parse.quote(str(parent_str), safe="'") if parent_str else ""
        async with session.get(url=fetch_url + parent_str) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ConnectionError


async def get_org(config, **kwargs) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=config.db.database_url + kwargs['org'] + "/" + str(kwargs["tg_id"])) as response:
            return await response.json()


async def get_count(config, org: str, region: str, city: str, page: int = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=config.db.database_url + org,
                               params={
                                   "user__region": region,
                                   "city": city,
                                   "page": 1 if page is None else page
                               }) as response:
            return await response.json()


async def status_update(config, tg_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"{config.db.database_url}users/{tg_id}",
                                 json={"is_subscribed": True}) as response:
            return await response.json()


async def add_product(config, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}products/", data=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                return None


async def add_agent(config, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}agents/", data=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                raise ConnectionError


async def get_my_products(config, tg_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}products/",
                               params={"distributor__user__tg_id": tg_id}) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ConnectionError


async def get_products(config, params=None):
    async with aiohttp.ClientSession() as session:
        print(params)
        async with session.get(url=f"{config.db.database_url}products/",
                               params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ConnectionError


async def get_one_product(config, product_name: str, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}new-products/{product_name}/",
                               params=params) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 404:
                return None
            else:
                raise ConnectionError


async def get_magazin(config, tg_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}magazin/{tg_id}/") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ConnectionError


async def get_one_magazin(config, magazin_name: str, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}new-magazin/{magazin_name}/",
                               params=params) as response:
            print(response.text, params)
            if response.status == 200:
                return await response.json()
            else:
                raise ConnectionError