from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


def pagination_reply_btn(data):
    content_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    results = data['results']
    for obj in results:
        content_btn.add(obj["name"])
    if data["next"] and data["previous"]:
        content_btn.add(KeyboardButton(_("⏮ Oldingi")), KeyboardButton(_("⏭ Keyingi")))
        content_btn.add(KeyboardButton(_("/start")))
        return content_btn
    if data["next"]:
        content_btn.add(KeyboardButton(_("⏭ Keyingi")))
    if data["previous"]:
        content_btn.add(KeyboardButton(_("⏮ Oldingi")))
    content_btn.add(KeyboardButton(_("/start")))
    return content_btn


async def paginated_response(m: Message, answer_text="", page=None):
    await m.answer(_("Privet"))
