from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from tgbot.keyboards.text import mahalla_dict
from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext

contact_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(_("Kontaktni yuborish 📱"), request_contact=True))

remove_btn = ReplyKeyboardRemove()


def lang_btns(back):
    lang_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("uz 🇺🇿"),
                                                             KeyboardButton("ru 🇷🇺"),
                                                             KeyboardButton("en 🇺🇸"))
    if back:
        lang_btn.add(KeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return lang_btn


organization_type_btns = ("Ishlab chiqaruvchi 🤵‍", "Distirbyutor 🔎", "Magazinchi 🙍‍♂",
                          ...,
                          )


def main_menu_btns(locale=None):
    main_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(_("Ishlab chiqaruvchi 🤵‍♂️", locale=locale)),
        KeyboardButton(_("Distirbyutor 🔎", locale=locale)),
        KeyboardButton(_("Magazinchi 🙍‍♂️", locale=locale)))
    return main_menu_btn


def main_menu_buis_btns(locale=None):
    main_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(_("Distributor qidirish️", locale=locale)),
        KeyboardButton(_("Distributorga so'rov yuborish", locale=locale)))
    return main_menu_btn


def my_product_menu_btns(locale=None, agents_count=0):
    main_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    if agents_count < 25:
        main_menu_btn.add(KeyboardButton(_("Agent qo'shish", locale=locale)))
        main_menu_btn.add(KeyboardButton(_("Mahsulotni o'chirish", locale=locale)))
    main_menu_btn.add(KeyboardButton(_("/start", locale=locale)))
    return main_menu_btn


def industry_kb(industries, lang, current_lvl=0):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for industry in industries:
        industry_btn.insert(industry[f"name_{lang}"])
    industry_btn.insert(KeyboardButton(_("/start")))
    return industry_btn


def products_kb(industries, lang):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for industry in industries:
        industry_btn.insert(industry["name"])
    industry_btn.insert("/start")
    return industry_btn


def distributer_start_btn(lang):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    industry_btn_texts = (
        _("Mening maxsulotlarim", locale=lang),
        _("Maxsulot qo'shish", locale=lang),
        _("Magazin qidirish", locale=lang),
        _("Maxsulot so'rash", locale=lang))
    for btn in industry_btn_texts:
        industry_btn.insert(KeyboardButton(btn))
    return industry_btn


def seller_start_btn(lang):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    industry_btn_texts = (
        _("Maxsulot qidirish", locale=lang),
        _("Maxsulot so'rash", locale=lang))
    for btn in industry_btn_texts:
        industry_btn.insert(KeyboardButton(btn))
    return industry_btn


region_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("Shahrisabz tumani")),
                                                           KeyboardButton(_("Shahrisabz shahri")),
                                                           KeyboardButton(_("Qarshi tumani")),
                                                           KeyboardButton(_("Qarshi Shahar")),
                                                           KeyboardButton(_("Qamashi tumani")),
                                                           KeyboardButton(_("Koson tumani")),
                                                           KeyboardButton(_("Ko'kdala tumani")),
                                                           KeyboardButton(_("Muborak tumani")),
                                                           KeyboardButton(_("Mirishkor tumani")),
                                                           KeyboardButton(_("Nishon tumani")),
                                                           KeyboardButton(_("Chiroqchi tumani")),
                                                           KeyboardButton(_("Yakkabog' tumani")),
                                                           KeyboardButton(_("Kitob tumani")),
                                                           KeyboardButton(_("Kasbi tumani")),
                                                           KeyboardButton(_("Guzar tumani")),
                                                           KeyboardButton(_("Dehqonobod tumani")),
                                                           KeyboardButton(_("/start")))

city_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("Toshkent sh")),
                                                         KeyboardButton(_("Toshkent v")),
                                                         KeyboardButton(_("Andijon")),
                                                         KeyboardButton(_("Buxoro")),
                                                         KeyboardButton(_("Farg'ona")),
                                                         KeyboardButton(_("Jizzax")),
                                                         KeyboardButton(_("Namangan")),
                                                         KeyboardButton(_("Navoiy")),
                                                         KeyboardButton(_("Qashqadaryo")),
                                                         KeyboardButton(_("Qoraqalpogʻiston R", )),
                                                         KeyboardButton(_("Samarqand")),
                                                         KeyboardButton(_("Sirdaryo")),
                                                         KeyboardButton(_("Surxondaryo")))

skip_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("O'tkazib yuborish")))

submit_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("✅Jo'natish")),
                                                           KeyboardButton(_("❌Bekor qilish")))


def mahalla_kb(shahar):
    sub_cats_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    mahallalar: list = mahalla_dict.get(shahar, [])
    for mahalla in mahallalar:
        sub_cats_kb.insert(KeyboardButton(mahalla))
    sub_cats_kb.insert(KeyboardButton(_("/start")))
    return sub_cats_kb


buy_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("Pay me"),
    KeyboardButton(_("/start")))

buis_get_info_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(_("Qaysi distirbyutorga sizning sohangiz kerak")),
    KeyboardButton(_("/start")))

delete_submit_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(_("Ha ✅")),
    KeyboardButton(_("Yo'q ❌")))


# def buis_pro(res):
#     buis_pro_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton(_("🔙 Orqaga")))
#     for i in res:
#         buis_pro_kb.insert(KeyboardButton(f"{i.id}. {i.name}"))
#     return buis_pro_kb
