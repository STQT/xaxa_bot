import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.db_cmds import get_user
from tgbot.filters.back import BackFilter
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
        user = await get_user(m.from_user.id)
        if user.type == "Ishlab chiqaruvchi 🤵‍♂️":
            await m.answer(_("Qaysi viloyatdan distirbyutor qidiryapsiz? 👇"), reply_markup=citys_btn)
            return await UserBuisState.get_interested_region.set()
        elif user.type == "Distirbyutor 🔎":
            await m.answer(_("Qaysi viloyat sizga qiziq?"), reply_markup=citys_btn)
            return await UserDistState.get_region.set()
        else:
            await m.answer(_("Qaysi viloyatdan distribyuter sizga qiziq?"), reply_markup=citys_btn)
            return await UserSellerState.get_region.set()


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
        return await UserSellerState.get_region.set()
    await m.answer(_("Qaysi viloyatda faoliyat yuritasiz? 🏭", locale=data["lang"]), reply_markup=citys_btn)
    if data["type"] == "Distirbyutor 🔎":
        return await UserDistState.get_region.set()
    return await UserBuisState.get_region.set()


def register_reg(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_lang, BackFilter(), state=UserLangState.get_lang)
    dp.register_message_handler(get_type, BackFilter(), state=UserMenuState.get_menu)
    dp.register_message_handler(get_name, state=UserParamsState.get_name)
    dp.register_message_handler(get_phone, content_types='contact', state=UserParamsState.get_phone)
    dp.register_message_handler(get_code, state=UserParamsState.get_code)
