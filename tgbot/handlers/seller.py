from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentTypes

from tgbot.db.db_api import *
from tgbot.filters.back import BackFilter
from tgbot.keyboards.reply import *
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import *

_ = i18ns.gettext


async def get_sell_address(m: Message, state: FSMContext, config, user):
    json_data = {
        "tg_id": m.from_user.id,
        "tg_name": m.from_user.full_name,
        "distreet": m.text,
        "city": m.text,
    }
    count = await get_count(config, "check-distributes", user["region"])
    await state.update_data(street=m.text)
    await pre_register_user(config, user_type="magazin", data=json_data)
    # res = await get_count_dist(data["region"], m.text)
    await m.answer(_("Distribyutrerlar soni {count} ta.\nTo'liq ma'lunot olish uchun Pro versiya harid qiling").
                   format(count=count["count"]), reply_markup=buy_kb)
    await UserSellerState.next()


async def get_buy_sell(m: Message, state: FSMContext, config):
    price = LabeledPrice(label="Pro podpiska uchun to'lov", amount=100 * 100)
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgWGCXrpS2g54YYm0eTzAHHFzY7Kj3ZXEcbg&usqp=CAU" if \
        m.text == "click" else "https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg"
    token = config.misc.click if m.text == "click" else config.misc.payme
    await state.update_data(pay_type=m.text)
    msg = await m.bot.send_invoice(chat_id=m.from_user.id, photo_url=photo, currency="rub", title="PRO",
                                   description="Pro uchun tolov",
                                   payload="test-invoice-payload", provider_token="1744374395:TEST:7ef02551931750210425",
                                   prices=[price])
    await state.update_data()
    await UserSellerState.next()


async def pre_checkout_query(query: PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(query.id, ok=True)
    await UserSellerState.next()


async def success_payment(m: Message, config, user_lang):
    await status_update(config, m.from_user.id)
    await m.delete()
    await m.answer(_("Siz oylik patpiskaga a'zo bo'ldingiz!"))
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Yo'nalishni tanlang 👇"), reply_markup=industry_kb(industries, user_lang))
    await UserSellerState.next()


async def get_sell_interested_industry(m: Message, config, user_lang):
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Sohani tanlang 👇"), reply_markup=industry_kb(industries, user_lang))
    await UserBuisState.next()


async def get_sell_interested_sub_industry(m: Message, config, user_lang):
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Sohani tanlang 👇"), reply_markup=industry_kb(industries, user_lang, 1))
    await UserBuisState.next()


async def get_sell_interested_product(m: Message, config, user_lang):
    industries = await get_industries(config, user_lang, m.text)
    await m.answer(_("Tovarni tanlang 👇"), reply_markup=industry_kb(industries, user_lang, 1))
    await UserBuisState.next()


def register_seller(dp: Dispatcher):
    dp.register_message_handler(get_sell_address, state=UserSellerState.get_street)
    dp.register_message_handler(get_buy_sell, state=UserSellerState.get_pay)
    dp.register_pre_checkout_query_handler(pre_checkout_query, state=UserSellerState.get_pay_conf)
    dp.register_message_handler(success_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT,
                                state=UserSellerState.get_success)
    dp.register_message_handler(get_sell_interested_industry, state=UserSellerState.get_interested_industry)
    dp.register_message_handler(get_sell_interested_sub_industry, state=UserSellerState.get_interested_sub_industry)
    dp.register_message_handler(get_sell_interested_product, state=UserSellerState.get_interested_prod)
