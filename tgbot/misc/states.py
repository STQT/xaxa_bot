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


class UserSellerState(StatesGroup):
    get_street = State()
    get_mahalla = State()
    get_name = State()
    get_pay = State()
    get_pay_conf = State()
    get_success = State()
    get_interested_industry = State()
    get_interested_sub_industry = State()
    get_interested_prod = State()
    get_agents_prod = State()


class UserSearchMagazinPaymentState(StatesGroup):
    get_region = State()
    get_city = State()
    get_pay = State()
    get_pay_conf = State()
    get_success = State()
    get_magazines = State()


class UserDistState(StatesGroup):
    get_industry = State()
    get_sub_industry = State()
    get_prod_industry = State()
    get_prod_name = State()
    get_prod_photo = State()
    get_prod_description = State()
    get_agent_region = State()
    get_agent_city = State()
    # get_agent_distreet = State()
    get_agent_phone = State()
    get_supervisor = State()
    company_name = State()
    company_phone = State()


class UserDistProductRequest(StatesGroup):
    get_description = State()


class UserBuisProductRequest(StatesGroup):
    get_description = State()


class UserDistMainState(StatesGroup):
    get_main = State()
    get_my_products = State()


class UserSellMainState(StatesGroup):
    get_main = State()


class UserSendProductRequestState(StatesGroup):
    get_name = State()
    get_photo = State()
    get_description = State()
    submit = State()


class UserBuisMainState(StatesGroup):
    get_main = State()


class UserAddProductState(StatesGroup):
    get_name = State()
    get_photo = State()
    get_description = State()


class UserBuisState(StatesGroup):
    get_industry = State()
    get_sub_industry = State()
    get_prod_industry = State()
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
