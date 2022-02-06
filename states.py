from aiogram.dispatcher.filters.state import StatesGroup, State


class StateOn(StatesGroup):
    # Main user
    reg_sex = State()
    reg_age = State()
    reg_name = State()

    # partner
    reg_sex_partner = State()
    reg_age_partner = State()

