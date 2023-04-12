import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.db.db_cmds import *
from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *

_ = i18ns.gettext


async def user_start(m: Message, status):
    if status:
        await m.answer(_("Assalomu alaykum!\nIltimos tilni tanlang 👇"), reply_markup=lang_btns(False))
        await UserLangState.get_lang.set()
    else:
        await m.answer(_("Assalomu alaykum siz kimsiz?"), reply_markup=main_menu_btns(False))
        await UserMenuState.get_menu.set()


async def get_lang(c: CallbackQuery):
    await create_user(c.from_user.id, c.data)
    await c.message.edit_text(_("Assalomu alaykum siz kimsiz?", locale=c.data),
                              reply_markup=main_menu_btns(c.data))
    await UserMenuState.get_menu.set()


async def get_type(c: CallbackQuery, state: FSMContext):
    await state.update_data(type=c.data)
    await c.message.edit_text(_("Iltimos ismingizni kiriting!"))
    await UserParamsState.get_name.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer(_("Iltimos telefon raqamingizni kiriting 📲"), reply_markup=contact_btn)
    await UserParamsState.next()


async def get_phone(m: Message, state: FSMContext):
    code = random.randint(1000, 9999)
    await state.update_data(number=m.contact.phone_number, code=code)
    await m.answer(_("Iltimos telefon raqamingizga kelgan kodni kiriting 📥"), reply_markup=remove_btn)
    await m.answer(text=str(code))
    await UserParamsState.next()


async def get_code(m: Message, state: FSMContext):
    data = await state.get_data()
    if str(data["code"]) != str(m.text):
        return await m.answer(_("Xato kod kiritildi 🚫"))
    if data["type"] == "seller":
        await m.answer(_("Sizning magaziningiz qaysi tumanda joylashgan? 🏬"), reply_markup=city_btn)
        await UserSellerState.get_region.set()
    elif data["type"] == "dist":
        await m.answer(_("Siz qaysi sohada Distirbyutorsiz? 📋"))
        await UserDistState.get_type.set()
    else:
        await m.answer(_("Siz qaysi sohada ishlab chiqarasiz? 🏭"))
        await UserBuisState.get_type.set()


async def get_region(c: CallbackQuery, state: FSMContext):
    await state.update_data(region=c.data)
    quarters = await get_quarters(c.data)
    await c.message.edit_text(_("Iltimos mahallani tanlang"), reply_markup=quarters_kb(quarters))
    await UserSellerState.next()


async def get_quarter(c: CallbackQuery, state: FSMContext):
    await state.update_data(address=c.data)
    await c.message.edit_text("Manzilingizni yuboring")
    await UserSellerState.next()


async def get_address(m: Message, state: FSMContext):
    data = await state.get_data()
    config = m.bot.get("config")
    await m.bot.send_message(config.tg_bot.group_ids, text=f"📋 <b>Magazinchidan sorov</b>.\n"
                                                           f"👤 Ism: {data['name']}\n"
                                                           f"📱 Raqam: {data['number']}\n"
                                                           f"🏢 Tuman: {data['region']}\n"
                                                           f"🏪 Mahalla: {data['address']}"
                                                           f"📍 Manzil: {m.text}\n")
    await m.answer(_("Tez orada agentimiz siz bilan bog'lanadi 👨‍💻"
                     "\nva sizning do'koningizga eng yaxshi mollar 📦"
                     "\nkelishini istasangiz botimizdan foydalaning 🤖"
                     "\nva kerakli bo'lgan zakazlarni qabul qiling! 📋"), reply_markup=main_menu_btns())
    await UserMenuState.get_menu.set()


async def get_dist_type(m: Message, state: FSMContext):
    await state.update_data(dist_type=m.text)
    await m.answer(_("Qaysi shahar bilan qiziqmoqdasiz?"), reply_markup=city_btn)
    await UserDistState.next()


async def get_city(c: CallbackQuery, state: FSMContext):
    await state.update_data(city=c.data)
    text = ""
    if c.data == 'Kitob':
        text = "Bu do'kon kitob\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: G'aybulla aka\ntelefon raqami: +998995595353"
    elif c.data == 'Qarshi':
        text = "Bu do'kon kitob\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Ahmad aka\ntelefon raqami: +998995595353"
    elif c.data == 'Koson':
        text = "Bu do'kon koson\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Abduvali aka\ntelefon raqami: +998995595353"
    elif c.data == "Ko'kdala":
        text = "Bu do'kon kokdala\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Qahhor aka\ntelefon raqami: +998995595353"
    elif c.data == 'Mirishkor':
        text = "Bu do'kon mirishkor\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Doston aka\ntelefon raqami: +998995595353"
    elif c.data == 'Muborak':
        text = "Bu do'kon muborak\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Faybulla aka\ntelefon raqami: +998995595353"
    elif c.data == 'Nishon':
        text = "Bu do'kon nishon\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: G'aybulla aka\ntelefon raqami: +998995595353"
    elif c.data == 'Chiroqchi':
        text = "Bu do'kon chiroqchi\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Fathulla aka\ntelefon raqami: +998995595353"
    elif c.data == 'Yakkabog':
        text = "Bu do'kon yakkabog'\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Aslan aka\ntelefon raqami: +998995595353"
    elif c.data == 'Shaxriasabz t':
        text = "Bu do'kon shaxrisabz\ntuman asaka Mahalla fuqarolaridagi\n3 - tor ko'chada joylashgan.\nMagazinchi: Bayroq aka\ntelefon raqami: +998995595353"
    await c.message.edit_text(text=text, reply_markup=dist_pod_btn)
    await UserDistState.next()


async def get_buis_type(m: Message, state: FSMContext):
    await state.update_data(buis_type=m.text)
    await m.answer(f"{m.text} sohasi bo'yicha\nJamshid aka distirbyutor kuchli\nshu, insonga aloqaga chiqish uchun\nknopkani bosing",
                   reply_markup=buis_dist_btn)
    await UserBuisState.next()


async def get_btn(c: CallbackQuery, state: FSMContext):
    if c.data == "Jamshid":
        await c.message.edit_text("Jamshid aka distirbyutorning raqami: +998995595353\nular 500 ta magazin bn ishlaydi, magazinlar qashqadaryo\nning kitob shahrida joylashgan")
    else:
        await c.message.edit_text("1. pechenie\n2. shokolad", reply_markup=buis_pod_btn)


async def back(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_("Assalomu alaykum siz kimsiz?"), reply_markup=main_menu_btns(False))
    await UserMenuState.get_menu.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(get_lang, BackFilter(), state=UserLangState.get_lang)
    dp.register_callback_query_handler(get_type, BackFilter(), state=UserMenuState.get_menu)
    dp.register_message_handler(get_name, state=UserParamsState.get_name)
    dp.register_message_handler(get_phone, content_types='contact', state=UserParamsState.get_phone)
    dp.register_message_handler(get_code, state=UserParamsState.get_code)
    dp.register_callback_query_handler(get_region, BackFilter(), state=UserSellerState.get_region)
    dp.register_message_handler(get_address, state=UserSellerState.get_address)
    dp.register_callback_query_handler(get_quarter, BackFilter(), state=UserSellerState.get_quarter)
    dp.register_message_handler(get_dist_type, state=UserDistState.get_type)
    dp.register_callback_query_handler(get_city, BackFilter(), state=UserDistState.get_region)
    dp.register_message_handler(get_buis_type, state=UserBuisState.get_type)
    dp.register_callback_query_handler(get_btn, BackFilter(), state=UserBuisState.get_dist)
    dp.register_callback_query_handler(back, state="*")

