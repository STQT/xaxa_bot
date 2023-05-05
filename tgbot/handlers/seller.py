from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentTypes

from tgbot.db.db_cmds import *
from tgbot.filters.back import BackFilter
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *

_ = i18ns.gettext


async def get_sell_address(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(street=m.text)
    await create_user(tg_id=m.from_user.id, name=data["name"], lang=data["lang"], number=data["number"],
                      us_type="Magazinchi 🙍‍♂️", region=data["region"], street=m.text)
    res = await get_count_dist(data["region"], m.text)
    await m.answer(_("Distribyutrerlar soni {count} ta.\nTo'liq ma'lunot olish uchun Pro versiya harid qiling").
                   format(count=len(res)), reply_markup=buy_kb)
    await UserSellerState.next()


async def get_buy_sell(m: Message, state: FSMContext, config):
    price = LabeledPrice(label="Pro podpiska uchun to'lov", amount=100 * 100)
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgWGCXrpS2g54YYm0eTzAHHFzY7Kj3ZXEcbg&usqp=CAU" if \
        m.text == "click" else "https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg"
    token = config.misc.click if m.text == "click" else config.misc.payme
    await state.update_data(pay_type=m.text)
    await m.bot.send_invoice(chat_id=m.from_user.id, photo_url=photo, currency="rub", title="PRO",
                             description="Pro uchun tolov",
                             payload="test-invoice-payload", provider_token="1744374395:TEST:a7b07f1db0034c9dbfe1",
                             prices=[price])
    await UserSellerState.next()


async def pre_checkout_query(query: PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(query.id, ok=True)
    await UserSellerState.next()


async def success_payment(m: Message, state: FSMContext):
    data = await state.get_data()
    await update_user(m.from_user.id, "pro")
    await m.answer(_("Siz oylik patpiskaga a'zo bo'ldingiz"))
    res = await get_count_dist(data["region"], data["street"])
    print(res)
    await m.answer(
        _("{spec} sohasi bo'yicha {count} ta distribyter").format(spec=data["interested_prod"], count=len(res)),
        reply_markup=buis_pro(res))
    await UserBuisState.next()


def register_seller(dp: Dispatcher):
    dp.register_message_handler(get_sell_address, state=UserSellerState.get_street)
    dp.register_pre_checkout_query_handler(pre_checkout_query, state=UserSellerState.get_pay)
    dp.register_message_handler(success_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT,
                                state=UserSellerState.get_success)
