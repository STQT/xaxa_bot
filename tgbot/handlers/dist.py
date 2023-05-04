
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from tgbot.db.db_cmds import *
from tgbot.filters.back import BackFilter
# from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *
from tgbot.services.sms import send_code


_ = i18ns.gettext


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