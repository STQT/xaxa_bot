from typing import List

import aiohttp

import urllib.parse


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
        async with session.post(headers=headers,
                                url=f"{config.db.database_url}create-user/",
                                json={"tg_id": tg_id, "tg_name": name, "lang": user_lang, "phone": user_phone,
                                      "user_type": user_type,
                                      "region": region}) as response:
            if response.status == 201:
                return await response.json()
            return False


async def pre_register_user(config, user_type: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}{user_type}/", data=data) as response:
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


async def get_count(config, region: str, street: str, lang: str) -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=config.db.database_url,
                               params={"region": region, "street": street, "lang": lang}) as response:
            return await response.json()
