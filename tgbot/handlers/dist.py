from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_api import get_industries, add_product, add_agent, get_my_products, get_one_product
from tgbot.filters.back import BackFilter
# from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *

_ = i18ns.gettext


async def main_dist_start(m: Message, state: FSMContext, config, user_lang):
    if m.text == _("Mening maxsulotlarim", locale=user_lang):
        products = await get_my_products(config, str(m.from_user.id))
        await m.answer(_("Mening maxsulotlarim", locale=user_lang), reply_markup=products_kb(products, user_lang))
        await UserDistMainState.get_my_products.set()
    elif m.text == _("Maxsulot qo'shish", locale=user_lang):
        industries = await get_industries(config, user_lang)
        await m.answer(_("Siz qaysi sohada distirbyutersiz? 👇"), reply_markup=industry_kb(industries, user_lang))
        await UserDistState.get_industry.set()
    else:
        await m.answer(_("Magazin qidirish", locale=user_lang))
        await UserSearchMagazinState.get_region.set()


# Mahsulot
# 1 - step industry
async def get_dist_industry(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(parent_category=m.text)
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Yo'nalishni tanlang 👇"), reply_markup=industry_kb(industries, user_lang))
    await UserDistState.next()


# 1.1 Select sub_category
async def get_dist_sub_industry(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(parent_category=m.text)
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Tovarni tanlang 👇"), reply_markup=industry_kb(industries, user_lang, 1))
    await UserDistState.next()


# 1.2 Select product type
async def get_dist_prod_industry(m: Message, state: FSMContext, config):
    await state.update_data(category=m.text)
    await m.answer(_("Tovar nomini kiriting"), reply_markup=ReplyKeyboardRemove())
    await UserDistState.next()


# 2 Get product name
async def get_product_name(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(name=m.text)
    await m.answer(_("Mahsulot rasmini jo'nating"), reply_markup=None)
    await UserDistState.next()


# Get product photo
async def get_product_photo(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(photo=m.photo[-1]['file_id'])
    await m.answer(_("Mahsulot tavsifini yozing"), reply_markup=None)
    await UserDistState.next()


# Get product description
async def get_product_description(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(description=m.text)
    await m.answer(_("Agent xududini tanlang"), reply_markup=city_btn)
    await UserDistState.next()


# Get product agent region
async def get_product_agent_region(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(agent_region=m.text)
    await m.answer(_("Agent telefon raqamini yozing"), reply_markup=ReplyKeyboardRemove())
    await UserDistState.next()


# Get product agent phone
async def get_product_agent_phone(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(agent_phone=m.text)
    await m.answer(_("Supervayzer tel raqamini yozing"), reply_markup=None)
    await UserDistState.next()


# Get product agent phone
async def get_product_supervisor_phone(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(supervisor_phone=m.text)
    await m.answer(_("Korxona nomini yozing"), reply_markup=None)
    await UserDistState.next()


# Get organization name
async def get_organization_name(m: Message, state: FSMContext, config, user_lang):
    await state.update_data(org_name=m.text)
    await m.answer(_("Korxona tel raqamini yozing"), reply_markup=None)
    await UserDistState.next()


# Get organization name and send to API
async def get_organization_phone(m: Message, state: FSMContext, config, user_lang):
    data = await state.get_data()
    product_data = {
        "tg_id": m.from_user.id,
        "industry": data.get("category"),
        "name": data.get("name"),
        "description": data.get("description"),
        "photo_uri": data.get("photo")
    }

    product = await add_product(config, product_data)
    if product:
        agent_data = {
            "agent_region": data.get("agent_region"),
            "agent_phone": data.get("agent_phone"),
            "supervisor_phone": data.get("supervisor_phone"),
            "corp_name": data.get("org_name"),
            "corp_phone": m.text,
            "product_name": product["name"]
        }
        await add_agent(config, agent_data)
        await m.answer(_("Malumotlaringiz saqlandi"), reply_markup=distributer_start_btn(user_lang))
        await state.finish()
        await UserDistMainState.get_main.set()
    else:
        await m.answer(_("Server bilan bog'lanish yo'q. Qayta urunib ko'ring"))
        await main_dist_start(m, state, config, user_lang)


async def get_my_product_handler(m: Message, state: FSMContext, config, user_lang):
    product_name = m.text
    data = await get_one_product(config=config, product_name=product_name)
    description = (
        f"Maxsulot nomi: {data['name']}\n"
        f"Tavsif: {data['description']}\n"
        f"Soha: {data[f'category_{user_lang}']}\n"
    )

    await m.answer_photo(caption=description, photo=data["photo_uri"])
    for i in data["agents"]:
        agent_info = (
            f"Supervisor tel: {i['supervisor_phone']}\n"
            f"Agent region: {i['agent_region']}\n"
            f"Agent tel: {i['agent_phone']}\n"
            f"Korxona nomi: {i['corp_name']}\n"
            f"Korxona tel: {i['corp_phone']}\n"
        )
        await m.answer(agent_info)


# async def get_sub_cat(m: Message, state: FSMContext):
#     await state.update_data(sub_cat=m.text)
#     data = await state.get_data()
#     await m.answer(_("Sohani tanlang 👇", locale=data["lang"]), reply_markup=prod_cat_kb(m.text, data["cat"]))
#     if data["type"] == "Ishlab chiqaruvchi 🤵‍♂️":
#         return await UserBuisState.get_buis_prod.set()
#     return await UserDistState.get_prod.set()


# async def get_prod_buis(m: Message, state: FSMContext):
#     data = await state.get_data()
#     await create_user(m.from_user.id, data["lang"], data["name"], data["number"], data["type"], data["region"], m.text)
#     await m.answer(_("Qaysi viloyatdan distribyuter qidiryapsiz?"), reply_markup=citys_btn)
#     await UserBuisState.next()


# data = await state.get_data()
# json_data = {
#     "tg_id": m.from_user.id,
#     "industry": data["category"],
#     "tg_name": m.from_user.full_name,
#     "product_name": m.text
# }

def register_dist(dp: Dispatcher):
    dp.register_message_handler(main_dist_start, BackFilter(), state=UserDistMainState.get_main)
    dp.register_message_handler(get_my_product_handler, BackFilter(), state=UserDistMainState.get_my_products)
    dp.register_message_handler(get_dist_industry, BackFilter(), state=UserDistState.get_industry)
    dp.register_message_handler(get_dist_sub_industry, BackFilter(), state=UserDistState.get_sub_industry)
    dp.register_message_handler(get_dist_prod_industry, BackFilter(), state=UserDistState.get_prod_industry)
    dp.register_message_handler(get_product_name, BackFilter(), state=UserDistState.get_prod_name)
    dp.register_message_handler(get_product_photo, BackFilter(), content_types='photo',
                                state=UserDistState.get_prod_photo)
    dp.register_message_handler(get_product_description, BackFilter(), state=UserDistState.get_prod_description)
    dp.register_message_handler(get_product_agent_region, BackFilter(), state=UserDistState.get_agent_region)
    dp.register_message_handler(get_product_agent_phone, BackFilter(), state=UserDistState.get_agent_phone)
    dp.register_message_handler(get_product_supervisor_phone, BackFilter(), state=UserDistState.get_supervisor)
    dp.register_message_handler(get_organization_name, BackFilter(), state=UserDistState.company_name)
    dp.register_message_handler(get_organization_phone, BackFilter(), state=UserDistState.company_phone)
    # dp.register_message_handler(get_buis_sub_cat, BackFilter(), state=UserBuisState.get_sub_cat)
    # dp.register_message_handler(get_buis_prod, BackFilter(), state=UserBuisState.get_prod)
