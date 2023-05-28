from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


def pagination_reply_btn(data, obj_name="name"):
    content_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    results = data['results']
    for obj in results:
        content_btn.add(obj[obj_name])
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


def new_pagination_reply_btn(data):
    content_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    count = data["count"]
    if count <= 10:
        content_btn.add(KeyboardButton("📄 1-10"))
    else:
        for page in range(count // 10):
            first_value = "📄 " + str(page) + "1" if page != 0 else "📄 1"
            second_value = str(page * 10 + 10) if page != 0 else "10"
            content_btn.insert(KeyboardButton(first_value + "-" + second_value))
    content_btn.insert(KeyboardButton(_("/start")))
    return content_btn


async def paginated_response(m: Message, answer_text="", page=None):
    await m.answer(_("Privet"))
