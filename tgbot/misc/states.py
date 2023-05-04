from aiogram.dispatcher.filters.state import State, StatesGroup


class UserLangState(StatesGroup):
    get_lang = State()


class UserMenuState(StatesGroup):
    get_menu = State()


class UserParamsState(StatesGroup):
    get_name = State()
    get_phone = State()
    get_code = State()


class UserSellerState(StatesGroup):
    get_region = State()
    get_address = State()
    get_pay = State()
    get_pay_conf = State()
    get_success = State()


class UserDistState(StatesGroup):
    get_region = State()
    get_cat = State()
    get_sub_cat = State()
    get_prod = State()


class UserBuisState(StatesGroup):
    get_region = State()
    get_cat = State()
    get_sub_cat = State()
    get_prod = State()
    get_interested_region = State()
    get_interested_cat = State()
    get_interested_sub_cat = State()
    get_interested_prod = State()
    get_buy = State()
    get_buy_conf = State()
    get_success = State()
    get_dist = State()
    get_info = State()
    get_text = State()
