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
    get_market = State()


class UserDistState(StatesGroup):
    get_type = State()
    get_region = State()
    get_cat = State()


class UserBuisState(StatesGroup):
    get_type = State()
    get_dist = State()

