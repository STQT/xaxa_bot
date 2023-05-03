from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.db.db_api import get_prod_cats, get_prods
from tgbot.keyboards.text import textss
from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext


def lang_btns(back):
    lang_btn = InlineKeyboardMarkup(row_with=1).add(InlineKeyboardButton("uz 🇺🇿", callback_data="uz"),
                                                    InlineKeyboardButton("ru 🇷🇺", callback_data="ru"),
                                                    InlineKeyboardButton("en 🇺🇸", callback_data="en"))
    if back:
        lang_btn.add(InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return lang_btn


def main_menu_btns(locale=False):
    main_menu_btn = InlineKeyboardMarkup(row_width=1)
    if locale:
        main_menu_btn.add(
            InlineKeyboardButton(_("Ishlab chiqaruvchi 🤵‍♂️", locale=locale), callback_data="buis"),
            InlineKeyboardButton(_("Distirbyutor 🔎", locale=locale), callback_data="dist"),
            InlineKeyboardButton(_("Magazinchi 🙍‍♂️", locale=locale), callback_data="seller"))
    else:
        main_menu_btn.add(
            InlineKeyboardButton(_("Ishlab chiqaruvchi 🤵‍♂️"), callback_data="buis"),
            InlineKeyboardButton(_("Distirbyutor 🔎"), callback_data="dist"),
            InlineKeyboardButton(_("Magazinchi 🙍‍♂️"), callback_data="seller"))
    return main_menu_btn


def markets_kb(markets):
    market_kb = InlineKeyboardMarkup(row_width=3)
    text = ""
    for market in markets:
        text += f"\n\n\n🆔 id: {market.id}\n🏢 Korxona nomi: {market.name_uz}\n📍 Faoliyat manzili: {market.address}\n🤵‍♂️ Faoliyat turi: {market.type}\n" \
                f"📦 Faoliyat yo'nalishi: {market.activity}\n📱 Telefon raqam: {market.number}"
        market_kb.insert(InlineKeyboardButton(market.id, callback_data=market.id))
    market_kb.insert(InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return market_kb, text


def quarters_kb(quarters):
    quarter_kb = InlineKeyboardMarkup(row_width=2)
    for quarter in quarters:
        quarter_kb.insert(InlineKeyboardButton(quarter.name, callback_data=quarter.name))
    quarter_kb.add(InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return quarter_kb


city_btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Shahrisabz t", callback_data="Shahrisabz t"),
                                                 InlineKeyboardButton("Shahrisabz sh", callback_data="Shahrisabz sh"),
                                                 InlineKeyboardButton("Qarshi t", callback_data="Qarshi t"),
                                                 InlineKeyboardButton("Qarshi sh", callback_data="Qarshi sh"),
                                                 InlineKeyboardButton("Qamashi", callback_data="Qamashi"),
                                                 InlineKeyboardButton("Koson", callback_data="Koson"),
                                                 InlineKeyboardButton("Muborak", callback_data="Muborak"),
                                                 InlineKeyboardButton("Nishon", callback_data="Nishon"),
                                                 InlineKeyboardButton("Chiroqchi", callback_data="Chiroqchi"),
                                                 InlineKeyboardButton("Yakkabog'", callback_data="Yakkabog'"),
                                                 InlineKeyboardButton("Kitob", callback_data="Kitob"),
                                                 InlineKeyboardButton("Kasbi", callback_data="Kasbi"),
                                                 InlineKeyboardButton("Guzor", callback_data="Guzor"),
                                                 InlineKeyboardButton("Dehqonobod", callback_data="Dehqonobod"),
                                                 InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))

citys_btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Toshkent sh", callback_data="Toshkent sh"),
                                                  InlineKeyboardButton("Toshkent v", callback_data="Toshkent v"),
                                                  InlineKeyboardButton("Andijon", callback_data="Andijot"),
                                                  InlineKeyboardButton("Buxoro", callback_data="Buxoro"),
                                                  InlineKeyboardButton("Farg'ona", callback_data="Farg'ona"),
                                                  InlineKeyboardButton("Jizzax", callback_data="Jizzax"),
                                                  InlineKeyboardButton("Namangan", callback_data="Namnagan"),
                                                  InlineKeyboardButton("Navoiy", callback_data="Navoiy"),
                                                  InlineKeyboardButton("Qashqadaryo", callback_data="Qashqadaryo"),
                                                  InlineKeyboardButton("Qoraqalpogʻiston R", callback_data="Qoraqalpogʻiston R"),
                                                  InlineKeyboardButton("Samarqand", callback_data="Samarqand"),
                                                  InlineKeyboardButton("Sirdaryo", callback_data="Sirdaryo"),
                                                  InlineKeyboardButton("Surxondaryo", callback_data="Surxondaryo"))

dist_pod_btn = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Boshqa magazinlar", callback_data="Shahrisabawdz"),
    InlineKeyboardButton("Top 10 magazinlar", callback_data="Shahrisabasdez"),
    InlineKeyboardButton("top 100 Qashqadaryodagi magazinlar", callback_data="Sdawdhahrisabz"),
    InlineKeyboardButton("Menga mahsulot kerak", callback_data="Shahrisabaefdaz"),
    InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))

buis_dist_btn = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Jamshid aka distirbyutor", callback_data="Jamshid"),
    InlineKeyboardButton("Yana qaysi soha bilan qiziqyapsiz?", callback_data="pod"),
    InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))

buis_pod_btn = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Pechenie", callback_data="pecheniex"),
    InlineKeyboardButton("Shokolad", callback_data="shokolad"),
    InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))

cats_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Oziq - ovqat maxsulotlari", callback_data="food"),
    InlineKeyboardButton("Go'zallik", callback_data="beauty"),
    InlineKeyboardButton("Maishy kimyoviy moddalar", callback_data="chemist"),
    InlineKeyboardButton("Hayvonlar uchun maxsulotlar", callback_data="animals"))


def sub_cat_kb(text):
    sub_cats_kb = InlineKeyboardMarkup(row_width=1)
    for i in textss[text]:
        sub_cats_kb.insert(InlineKeyboardButton(i, callback_data=i))
    return sub_cats_kb


def prod_cat_kb(text, cat):
    prod_cats_kb = InlineKeyboardMarkup(row_width=1)
    for i in textss[cat][text]:
        prod_cats_kb.insert(InlineKeyboardButton(i, callback_data=i))
    return prod_cats_kb


food_cats_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Bakaleya", callback_data="bakaleya"),
    InlineKeyboardButton("Issiq ichimlikalr", callback_data="tea"),
    InlineKeyboardButton("Shirinliklar", callback_data="sweets"),
    InlineKeyboardButton("Quriq mevalar", callback_data="dry"),
    InlineKeyboardButton("Shirin konservalar", callback_data="sweet cons"),
    InlineKeyboardButton("Snelklar", callback_data="snacks"),
    InlineKeyboardButton("Bolalar ovqati", callback_data="children food"),
    InlineKeyboardButton("Sog'lom ovqatlanish", callback_data="healthy"),
    InlineKeyboardButton("Sut va sut maxsulotlari", callback_data="milk"),
    InlineKeyboardButton("Non va non maxsulotlari", callback_data="bred"),
    InlineKeyboardButton("Yarim tayyor maxsulotlar", callback_data="half"),
)

buy_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Pay me", callback_data="pay me"),
    InlineKeyboardButton("Click", callback_data="click"))

