import aiohttp
from aiohttp import BasicAuth


async def send_code(phone, code, config):
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003", "sms": {"originator": "3700", "content": {
            "text": f"Sizning xa xa botida ro'yxatdan o'tish kodingiz: {code}"}}}]}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=config.misc.sms_url, auth=BasicAuth(config.misc.sms_login, config.misc.sms_pass),
                                json=sms_data) as response:

            pass
