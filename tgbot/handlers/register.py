import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_api import create_user, get_industries, get_count
from tgbot.db.db_api import get_user
from tgbot.filters.back import BackFilter
from tgbot.handlers.dist import search_magazines_get_city
from tgbot.keyboards.reply import *
from tgbot.misc.content import paginated_response
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *
from tgbot.services.sms import send_code

_ = i18ns.gettext


async def user_start(m: Message, status, config):
    if status:
        await m.answer(_("Assalomu alaykum!\nIltimos tilni tanlang 👇"), reply_markup=lang_btns(False))
        await UserLangState.get_lang.set()
    else:
        user = await get_user(m.from_user.id, config)
        industries = await get_industries(config, user["lang"])
        if user["user_type"] == "business":
            if user["is_registered"]:
                await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_buis_btns(user["lang"]))
                await UserBuisMainState.get_main.set()
                return

            await m.answer(_("Siz qaysi sohada ishlab chiqarasiz? 👇"),
                           reply_markup=industry_kb(industries, user["lang"]))
            return await UserBuisState.get_industry.set()
        elif user["user_type"] == "distributor":
            if user["is_registered"]:
                await m.answer(_("Bo'limni tanlang"), reply_markup=distributer_start_btn(user["lang"]))
                return await UserDistMainState.get_main.set()
            await m.answer(_("Siz qaysi sohada distirbyutersiz? 👇"), reply_markup=industry_kb(industries, user["lang"]))
            await UserDistState.get_industry.set()
            return
        else:
            if user["is_registered"]:
                if user["is_subscribed"]:
                    await m.answer(_("Sohani tanlang 👇"), reply_markup=industry_kb(industries, user["lang"]))
                    return await UserSellerState.get_interested_industry.set()
                else:
                    count = await get_count(config, "check-distributes", user["region"], "")
                    await m.answer(_("{count} ta distribyutor. Bular haqida ma'lumot olish uchun PRO versiyani xarid"
                                     " qiling").format(count=count["count"]), reply_markup=buy_kb)
                    return await UserSellerState.get_pay.set()
            await m.answer(_("Qaysi tumandan distribyuter sizga qiziq? 👇"), reply_markup=region_btn)
            await UserSellerState.get_street.set()


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
    print(code)
    await state.update_data(number=m.contact.phone_number, code=code)
    await send_code(m.contact.phone_number, code, config)
    await m.answer(_("Iltimos telefon raqamingizga kelgan kodni kiriting 📥"), reply_markup=remove_btn)
    await UserParamsState.next()


async def get_code(m: Message, state: FSMContext):
    data = await state.get_data()
    if str(data["code"]) != str(m.text):
        return await m.answer(_("Xato kod kiritildi 🚫"))
    await m.answer(_("Qaysi viloyatda faoliyat yuritasiz? 🏭", locale=data["lang"]), reply_markup=city_btn)
    await UserParamsState.next()


async def get_region(m: Message, state: FSMContext, config):
    if m.text == "Qashqadaryo":
        data = await state.get_data()
        if data["type"] == "Ishlab chiqaruvchi 🤵‍♂️":
            user_type = "business"
        elif data["type"] == "Distirbyutor 🔎":
            user_type = "distributor"
        else:
            user_type = "magazin"
        user = await create_user(m.from_user.id, data["name"], data["lang"], data["number"], user_type, m.text, config)
        print(user, "asdasdas")
        mess, kb = "", ""
        industry = await get_industries(config, data["lang"])
        if data["type"] in ["Ishlab chiqaruvchi 🤵‍♂️"]:
            mess, kb = "Siz qaysi sohada ishlab chiqarasiz ?", industry_kb(industry, data["lang"])
            await UserBuisState.get_industry.set()
        elif data["type"] in ["Distirbyutor 🔎"]:
            mess, kb = "Siz qaysi sohada distirbyutersiz ?", industry_kb(industry, data["lang"])
            await UserDistState.get_industry.set()
        elif data["type"] in ["Magazinchi 🙍‍♂️"]:
            mess, kb = "Dokoningiz qaysi shaxarda joylashgan ?", region_btn
            await UserSellerState.get_street.set()
        await m.answer(mess, reply_markup=kb)
    else:
        return await m.answer("Tez orada! 😃")


def register_reg(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    # dp.register_message_handler(search_magazines_get_city, commands=["start"], state="*")
    dp.register_message_handler(get_lang, BackFilter(), state=UserLangState.get_lang)
    dp.register_message_handler(get_type, BackFilter(), state=UserMenuState.get_menu)
    dp.register_message_handler(get_name, state=UserParamsState.get_name)
    dp.register_message_handler(get_phone, content_types='contact', state=UserParamsState.get_phone)
    dp.register_message_handler(get_code, state=UserParamsState.get_code)
    dp.register_message_handler(get_region, state=UserParamsState.get_region)
