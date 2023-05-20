from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from tgbot.keyboards.text import textss
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


def my_product_menu_btns(locale=None):
    main_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(_("Agent qo'shish", locale=locale)),
        KeyboardButton(_("/start", locale=locale)))
    return main_menu_btn


def industry_kb(industries, lang, current_lvl=0):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for industry in industries:
        industry_btn.insert(industry[f"name_{lang}"])
    if current_lvl > 0:
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


region_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("Shahrisabz t")),
                                                           KeyboardButton(_("Shahrisabz sh")),
                                                           KeyboardButton(_("Qarshi t")),
                                                           KeyboardButton(_("Qarshi sh")),
                                                           KeyboardButton(_("Qamashi")),
                                                           KeyboardButton(_("Koson")),
                                                           KeyboardButton(_("Muborak")),
                                                           KeyboardButton(_("Nishon")),
                                                           KeyboardButton(_("Chiroqchi")),
                                                           KeyboardButton(_("Yakkabog'")),
                                                           KeyboardButton(_("Kitob")),
                                                           KeyboardButton(_("Kasbi")),
                                                           KeyboardButton(_("Guzor")),
                                                           KeyboardButton(_("Dehqonobod")),
                                                           KeyboardButton(_("🔙 Orqaga")))

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

distreet_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(_("O'tkazib yuborish")))


def sub_cat_kb(text):
    sub_cats_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in textss[text]:
        sub_cats_kb.insert(KeyboardButton(i))
    sub_cats_kb.insert(KeyboardButton(_("🔙 Orqaga")))
    return sub_cats_kb


def prod_cat_kb(text, cat):
    prod_cats_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in textss[cat][text]:
        prod_cats_kb.insert(KeyboardButton(i))
    prod_cats_kb.insert(KeyboardButton(_("🔙 Orqaga")))
    return prod_cats_kb


buy_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("Pay me"),
    KeyboardButton(_("🔙 Orqaga")))

buis_get_info_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(_("Qaysi distirbyutorga sizning sohangiz kerak")),
    KeyboardButton(_("🔙 Orqaga")))


def buis_pro(res):
    buis_pro_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton(_("🔙 Orqaga")))
    for i in res:
        buis_pro_kb.insert(KeyboardButton(f"{i.id}. {i.name}"))
    return buis_pro_kb
