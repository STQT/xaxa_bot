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


def main_menu_btns(locale=None):
    main_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(_("Ishlab chiqaruvchi 🤵‍♂️", locale=locale)),
        KeyboardButton(_("Distirbyutor 🔎", locale=locale)),
        KeyboardButton(_("Magazinchi 🙍‍♂️", locale=locale)))
    return main_menu_btn


def industry_kb(industries, lang):
    industry_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for industry in industries:
        industry_btn.insert(industry[f"name_{lang}"])
    return industry_btn


def markets_kb(markets):
    market_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    text = ""
    for market in markets:
        text += f"\n\n\n🆔 id: {market.id}\n🏢 Korxona nomi: {market.name_uz}\n📍 Faoliyat manzili: {market.address}\n🤵‍♂️ Faoliyat turi: {market.type}\n" \
                f"📦 Faoliyat yo'nalishi: {market.activity}\n📱 Telefon raqam: {market.number}"
        market_kb.insert(KeyboardButton(market.id))
    market_kb.insert(KeyboardButton(_("🔙 Orqaga")))
    return market_kb, text


def quarters_kb(quarters):
    quarter_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for quarter in quarters:
        quarter_kb.insert(KeyboardButton(quarter.name))
    quarter_kb.add(KeyboardButton(_("🔙 Orqaga")))
    return quarter_kb


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

dist_pod_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Boshqa magazinlar"),
    KeyboardButton("Top 10 magazinlar"),
    KeyboardButton("top 100 Qashqadaryodagi magazinlar"),
    KeyboardButton("Menga mahsulot kerak"),
    KeyboardButton(_("🔙 Orqaga")))

buis_dist_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Jamshid aka distirbyutor"),
    KeyboardButton("Yana qaysi soha bilan qiziqyapsiz?"),
    KeyboardButton(_("🔙 Orqaga")))

buis_pod_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Pechenie", callback_data="pechenie"),
    KeyboardButton("Shokolad", callback_data="shokolad"),
    KeyboardButton(_("🔙 Orqaga"), callback_data="back"))

cats_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Oziq - ovqat maxsulotlari"),
    KeyboardButton("Go'zallik"),
    KeyboardButton("Maishy kimyoviy moddalar"),
    KeyboardButton("Hayvonlar uchun maxsulotlar"),
    KeyboardButton(_("🔙 Orqaga")))


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


food_cats_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Bakaleya"),
    KeyboardButton("Issiq ichimlikalr"),
    KeyboardButton("Shirinliklar"),
    KeyboardButton("Quriq mevalar"),
    KeyboardButton("Shirin konservalar"),
    KeyboardButton("Sneklar"),
    KeyboardButton("Bolalar ovqati"),
    KeyboardButton("Sog'lom ovqatlanish"),
    KeyboardButton("Sut va sut maxsulotlari"),
    KeyboardButton("Non va non maxsulotlari"),
    KeyboardButton("Yarim tayyor maxsulotlar"))

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
