import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_cmds import *
from tgbot.filters.back import BackFilter
# from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *
from tgbot.services.sms import send_code

_ = i18ns.gettext


async def user_start(m: Message, status):
    if status:
        await m.answer(_("Assalomu alaykum!\nIltimos tilni tanlang 👇"), reply_markup=lang_btns(False))
        await UserLangState.get_lang.set()
    else:
        await m.answer(_("Qaysi viloyatdan distirbyutor qidiryapsiz? 👇"), reply_markup=citys_btn)
        return await UserBuisState.get_region.set()


async def get_lang(m: Message, state: FSMContext):
    lang = m.text[:2]
    await state.update_data(lang=lang)
    await m.answer(_("Assalomu alaykum siz kimsiz?", locale=lang), reply_markup=main_menu_btns(lang))
    await UserMenuState.get_menu.set()


async def get_type(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(type=m.text)
    await m.answer(_("Iltimos ismingizni kiriting!", locale=data["lang"]), reply_markup=remove_btn)
    await UserParamsState.get_name.set()


async def get_name(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(name=m.text)
    await m.answer(_("Iltimos telefon raqamingizni kiriting 📲", locale=data["lang"]), reply_markup=contact_btn)
    await UserParamsState.next()


async def get_phone(m: Message, state: FSMContext, config):
    code = random.randint(1000, 9999)
    await state.update_data(number=m.contact.phone_number, code=code)
    await send_code(m.contact.phone_number, code, config)
    await m.answer(_("Iltimos telefon raqamingizga kelgan kodni kiriting 📥"), reply_markup=remove_btn)
    await UserParamsState.next()


async def get_code(m: Message, state: FSMContext):
    data = await state.get_data()
    if str(data["code"]) != str(m.text):
        return await m.answer(_("Xato kod kiritildi 🚫"))
    if data["type"] == "Magazinchi 🙍‍♂️":
        await m.answer(_("Sizning magaziningiz qaysi shaharda joylashgan? 🏬", locale=data["lang"]),
                       reply_markup=citys_btn)
    else:
        await m.answer(_("Qaysi viloyatda faoliyat yuritasiz? 🏭", locale=data["lang"]), reply_markup=citys_btn)
    await UserParamsState.next()


async def get_region(m: Message, state: FSMContext):
    if m.text == "Qashqadaryo":
        await state.update_data(region=m.text)
        data = await state.get_data()
        if data["type"] == "Magazinchi 🙍‍♂️":
            await get_count(m.text, "Distirbyutor 🔎")
            await m.answer(_("Tumanni tanlang 👇"), reply_markup=city_btn)
            return await UserSellerState.get_address.set()
        await m.answer(_("Sohani tanlang 👇", locale=data["lang"]), reply_markup=cats_kb)
        return await UserParamsState.next()
    else:
        return await m.answer("Tez orada! 😃")


async def get_sel_address(m: Message, state: FSMContext):
    await state.update_data(sell_street=m.text)
    await m.answer()


async def get_sel_buy(m: Message, state: FSMContext):
    await update_user(m.from_user.id, "pro")
    data = await state.get_data()
    await m.answer(_("Siz Pro potpiskaga azo bo'ldingiz!\n"))
    await m.answer(_("{prod} soha bo'yicha Jamshid aka\n📲 Raqam: +98900000000\n🏬 Magazinlar: 10 ta\n"
                     "📍 Manzil: Koson tumani, yangiariq ko'chasi").format(prod=data["buis_prod"]),
                   reply_markup=buis_get_info_kb)
    await UserBuisState.next()

async def get_cat(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(cat=m.text)
    await m.answer(_("Sohani tanlang 👇", locale=data["lang"]), reply_markup=sub_cat_kb(m.text))
    await UserParamsState.next()


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


async def get_region_buis(m: Message, state: FSMContext):
    if m.text != "Qashqadaryo":
        return await m.answer("Tez orada! 😃")
    await m.answer(_("Qaysi sohada?"), reply_markup=cats_kb)
    await UserBuisState.get_cat.set()


async def get_buis_cat(m: Message, state: FSMContext):
    await state.update_data(buis_cat=m.text)
    await m.answer(_("Sohani tanlang 👇"), reply_markup=sub_cat_kb(m.text))
    await UserBuisState.next()


async def get_buis_sub_cat(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(buis_sub_cat=m.text)
    await m.answer(_("Sohani tanlang 👇"), reply_markup=prod_cat_kb(m.text, data["buis_cat"]))
    await UserBuisState.next()


async def get_buis_prod(m: Message, state: FSMContext, user):
    data = await state.get_data()
    if user.status == "basic":
        await state.update_data(buis_prod=m.text)
        await m.answer(f"{m.text} sohasi bo'yicha 50 ta distribyuter bor ularni ko'rish uchun PRO versiyani xarid qiling",
                       reply_markup=buy_kb)
        return await UserBuisState.next()
    await m.answer(_("{prod} soha bo'yicha Jamshid aka\n📲 Raqam: +98900000000\n🏬 Magazinlar: 10 ta\n"
                     "📍 Manzil: Koson tumani, yangiariq ko'chasi").format(prod=data["buis_prod"]),
                   reply_markup=buis_get_info_kb)
    await UserBuisState.get_info.set()


async def get_buis_info(m: Message):
    await m.answer(_("O'zingiz haqingizda ma'lumot qoldiring distirbyutorlarga ma'lumotlaringiz qiziq bo'lsa aloqaga "
                     "chiqishadi! 👨‍💻"), reply_markup=remove_btn)
    await UserBuisState.next()


async def send_buis(m: Message, user, config):
    await m.bot.send_message(chat_id=config.tg_bot.buis_ids, text=f"👤 Ismi: {user.name}\n📲 Raqam: {user.number}\n"
                                                                  f"📦 Tovar: {user.product}\n🌆 Shahar: {user.region}\n"
                                                                  f"💬 Ma'lumot: {m.text}")
    await m.answer(_("So'rovingiz distribyuterlarga yetkazildi!"), reply_markup=citys_btn)
    await UserBuisState.next()


async def get_buy_buis(m: Message, state: FSMContext):
    await update_user(m.from_user.id, "pro")
    data = await state.get_data()
    await m.answer(_("Siz Pro potpiskaga azo bo'ldingiz!\n"))
    await m.answer(_("{prod} soha bo'yicha Jamshid aka\n📲 Raqam: +98900000000\n🏬 Magazinlar: 10 ta\n"
                     "📍 Manzil: Koson tumani, yangiariq ko'chasi").format(prod=data["buis_prod"]), reply_markup=buis_get_info_kb)
    await UserBuisState.next()


async def back(m: Message, state: FSMContext):
    data = await state.get_data()
    state = await state.get_state()
    if state == "UserParamsState:get_sub_cat":
        await m.answer(_("Sohani tanlang 👇"), reply_markup=cats_kb)
        return await UserParamsState.get_cat.set()
    elif state == "UserBuisState:get_buis_prod":
        await m.answer(_("Sohani tanlang 👇"), reply_markup=sub_cat_kb(data["cat"]))
        return await UserParamsState.get_sub_cat.set()
    elif state in ["UserBuisState:get_buy", "UserBuisState:get_cat"]:
        await m.answer(_("Qaysi viloyatdan distribyuter qidiryapsiz?"), reply_markup=citys_btn)
        return await UserBuisState.get_region.set()
    elif state == "UserBuisState:get_sub_cat":
        await m.answer(_("Sohani tanlang 👇"), reply_markup=cats_kb)
        return await UserBuisState.get_cat.set()
    elif state == "UserBuisState:get_prod":
        await m.answer(_("Sohani tanlang 👇"), reply_markup=sub_cat_kb(data["buis_cat"]))
        return await UserBuisState.get_sub_cat.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_lang, BackFilter(), state=UserLangState.get_lang)
    dp.register_message_handler(get_type, BackFilter(), state=UserMenuState.get_menu)
    dp.register_message_handler(get_name, state=UserParamsState.get_name)
    dp.register_message_handler(get_phone, content_types='contact', state=UserParamsState.get_phone)
    dp.register_message_handler(get_code, state=UserParamsState.get_code)
    dp.register_message_handler(get_region, BackFilter(), state=UserParamsState.get_region)
    dp.register_message_handler(get_cat, BackFilter(), state=UserParamsState.get_cat)
    dp.register_message_handler(get_sub_cat, BackFilter(), state=UserParamsState.get_sub_cat)
    dp.register_message_handler(get_prod_buis, BackFilter(), state=UserBuisState.get_buis_prod)
    dp.register_message_handler(get_region_buis, BackFilter(), state=UserBuisState.get_region)
    dp.register_message_handler(get_buis_cat, BackFilter(), state=UserBuisState.get_cat)
    dp.register_message_handler(get_buis_sub_cat, BackFilter(), state=UserBuisState.get_sub_cat)
    dp.register_message_handler(get_buis_prod, BackFilter(), state=UserBuisState.get_prod)
    dp.register_message_handler(get_buy_buis, BackFilter(), state=UserBuisState.get_buy)
    dp.register_message_handler(get_buis_info, BackFilter(), state=UserBuisState.get_info)
    dp.register_message_handler(send_buis, BackFilter(), state=UserBuisState.get_text)
    dp.register_message_handler(back, state="*")
