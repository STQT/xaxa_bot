from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_api import get_my_products
from tgbot.keyboards.reply import my_product_menu_btns, products_kb

from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext


async def product_answer(m, data, user_lang):
    description = (
        f"Maxsulot nomi: {data['name']}\n"
        f"Tavsif: {data['description']}\n"
        f"Soha: {data[f'category_{user_lang}']}\n"
    )
    await m.answer_photo(caption=description, photo=data["photo_uri"])
    sended_agents = 0
    for i in data["agents"]:
        agent_info = (
            f"{sended_agents + 1}. Supervisor tel: {i['supervisor_phone']}\n"
            f"Agent region: {i['agent_region']}\n"
            f"Agent shaxar: <b>{i['agent_city']}</b>\n"
            # f"Agent tuman: {i['agent_distreet']}\n"
            f"Agent tel: {i['agent_phone']}\n"
            f"Korxona nomi: {i['corp_name']}\n"
            f"Korxona tel: {i['corp_phone']}\n"
        )
        await m.answer(agent_info)
        sended_agents += 1
    await m.answer("Ushbu maxsulot bilan qanday amal bajarasiz?",
                   reply_markup=my_product_menu_btns(user_lang, agents_count=sended_agents))


async def get_my_products_kbs(m: Message, state: FSMContext, config, user_lang):
    products = await get_my_products(config, str(m.from_user.id))
    await m.answer(_("Mening maxsulotlarim", locale=user_lang), reply_markup=products_kb(products, user_lang))
