from aiogram.dispatcher.filters.state import State, StatesGroup


class UserLangState(StatesGroup):
    get_lang = State()


class UserMenuState(StatesGroup):
    get_menu = State()


class UserParamsState(StatesGroup):
    get_name = State()
    get_phone = State()
    get_code = State()
    get_region = State()
    get_cat = State()
    get_sub_cat = State()


class UserSellerState(StatesGroup):
    get_address = State()
    get_
    get_pay = State()


class UserDistState(StatesGroup):
    get_prod = State()


class UserBuisState(StatesGroup):
    get_buis_prod = State()
    get_region = State()
    get_cat = State()
    get_sub_cat = State()
    get_prod = State()
    get_buy = State()
    get_info = State()
    get_text = State()
