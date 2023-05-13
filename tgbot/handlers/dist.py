from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_api import get_industries, pre_register_user
from tgbot.db.db_cmds import *
from tgbot.filters.back import BackFilter
# from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *

_ = i18ns.gettext


async def main_dist_start(m: Message, state: FSMContext, config, user_lang):
    # await state.update_data(category=m.text)
    # industries = await get_industries(config, user_lang, m.text)
    # await m.answer(_("Bo'limni tanlang"), reply_markup=industry_kb(industries, user_lang))
    # await UserDistState.next()
    if m.text == _("Mening maxsulotlarim", locale=user_lang):
        await m.answer(_("Mening maxsulotlarim", locale=user_lang))
        await UserDistMainState.get_my_products.set()
    elif m.text == _("Maxsulot qo'shish", locale=user_lang):
        await m.answer(_("Maxsulot qo'shish", locale=user_lang))
        await UserAddProductState.get_name.set()
    else:
        await m.answer(_("Magazin qidirish", locale=user_lang))
        await UserDistMainState.get_search_magazines.set()



async def get_dist_industry(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(category=m.text)
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Yo'nalishni tanlang 👇"), reply_markup=industry_kb(industries, user_lang))
    await UserDistState.next()


async def get_dist_sub_industry(m: Message, state: FSMContext, config, user_lang):
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Tovarni tanlang 👇"), reply_markup=industry_kb(industries, user_lang, 1))
    await UserDistState.next()


async def get_dist_prod_industry(m: Message, state: FSMContext, config):
    data = await state.get_data()
    json_data = {
        "tg_id": m.from_user.id,
        "industry": data["category"],
        "tg_name": m.from_user.full_name,
        "product_name": m.text
    }

    res = await pre_register_user(config, user_type="distributor", data=json_data)
    print(res)
    await m.answer(_("Tovar nomini kiriting"), reply_markup=city_btn)
    await UserDistState.next()


async def get_sub_cat(m: Message, state: FSMContext):
    await state.update_data(sub_cat=m.text)
    data = await state.get_data()
    await m.answer(_("Sohani tanlang 👇", locale=data["lang"]), reply_markup=prod_cat_kb(m.text, data["cat"]))
    if data["type"] == "Ishlab chiqaruvchi 🤵‍♂️":
        return await UserBuisState.get_buis_prod.set()
    return await UserDistState.get_prod.set()


async def get_prod_buis(m: Message, state: FSMContext):
    data = await state.get_data()
    await create_user(m.from_user.id, data["lang"], data["name"], data["number"], data["type"], data["region"], m.text)
    await m.answer(_("Qaysi viloyatdan distribyuter qidiryapsiz?"), reply_markup=citys_btn)
    await UserBuisState.next()


def register_dist(dp: Dispatcher):
    dp.register_message_handler(get_dist_industry, BackFilter(), state=UserDistState.get_industry)
    dp.register_message_handler(get_dist_sub_industry, BackFilter(), state=UserDistState.get_sub_industry)
    dp.register_message_handler(get_dist_prod_industry, BackFilter(), state=UserDistState.get_prod_industry)
    dp.register_message_handler(main_dist_start, BackFilter(), state=UserDistMainState.get_main)
    # dp.register_message_handler(get_buis_sub_cat, BackFilter(), state=UserBuisState.get_sub_cat)
    # dp.register_message_handler(get_buis_prod, BackFilter(), state=UserBuisState.get_prod)
