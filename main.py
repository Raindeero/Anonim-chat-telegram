import random

from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from DB import SQLite_db
from db_requests import GET_SEARCH_RESULT_REQ, GET_ALTER_SEARCH_RESULT_REQ, REG_NEW_USER_REQ, ADD_PARTNER_REQ
from models import UserData
from modules import dp
from states import StateOn
from temp import TempCash, UserTempData, SEX_DICT


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message, user_info: tuple):
    if user_info:
        await message.answer("Зарегистрирован")
        return

    await StateOn.reg_sex.set()

    keyboard_markup = types.InlineKeyboardMarkup()
    user_female_btn = types.InlineKeyboardButton('Я девушка', callback_data='user_female')
    user_male_btn = types.InlineKeyboardButton('Я парень', callback_data='user_male')
    keyboard_markup.add(user_female_btn, user_male_btn)

    await message.answer("Привет, какого ты пола?", reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('user_'), state=StateOn.reg_sex)
async def reg_sex(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    uid = callback_query.from_user.id
    sex = SEX_DICT.get(callback_query.data.replace("user_", ""))
    TempCash.insert(uid, UserTempData(uid, sex))

    await StateOn.reg_age.set()
    await callback_query.message.answer("Сколько тебе лет?")


@dp.message_handler(state=StateOn.reg_age)
async def checker_age(message: types.Message):
    age = message.text
    if not age.isdigit() or int(age) <= 0:
        await message.answer("Вы ввели не возраст")
        return

    uid = message.from_user.id
    TempCash.add_age(uid, int(age))

    await StateOn.reg_name.set()
    await message.answer("Как тебя зовут?")


@dp.message_handler(state=StateOn.reg_name)
async def checker_name(message: types.Message):
    name = message.text
    if len(name) > 20 or name.isdigit():
        await message.answer("Это имя не подходит")
        return

    TempCash.add_name(message.from_user.id, name)

    await StateOn.reg_sex_partner.set()

    data = [('Девушку', 'partner_female'), ('Парня', 'partner_male'), ('Все равно', 'partner_all')]
    keyboard_markup = InlineKeyboardMarkup().add(*[InlineKeyboardButton(text=x, callback_data=y) for x, y in data])

    await message.answer("Какого собеседника ты ищешь?", reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('partner_'), state=StateOn.reg_sex_partner)
async def reg_sex(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    sex = SEX_DICT.get(callback_query.data.replace("partner_", ""))
    TempCash.add_sex_partner(callback_query.from_user.id, sex)

    data = [(' < 18 ', 'age_loli'), (' 18-24 ', 'age_young'), (' 25-35 ', 'age_milf'), (' 36+ ', 'age_grandma')]
    keyboard_markup = InlineKeyboardMarkup(row_width=4).add(
        *[InlineKeyboardButton(text=x, callback_data=y) for x, y in data]
    )

    await StateOn.reg_age_partner.set()
    await callback_query.message.answer('Какого возраста?', reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('age_'), state=StateOn.reg_age_partner)
async def last_step(callback_query: types.CallbackQuery, db: SQLite_db):
    await callback_query.message.delete()
    ages = {'loli': (0, 17), 'young': (18, 24), 'milf': (25, 35), 'grandma': (36, 1000)}
    fu = TempCash.get_and_add_age_partner(
        callback_query.from_user.id, ages.get(callback_query.data.replace("age_", ""))
    )
    db.query(REG_NEW_USER_REQ, [fu.uid, fu.sex.value, fu.name, fu.age, fu.sex_partner.value, *fu.age_partner])
    kb = ReplyKeyboardMarkup().add('Найти собеседника')
    await callback_query.message.answer('Регистрация прошла успешнo', reply_markup=kb)


@dp.message_handler(Text('Найти собеседника'))
async def finder(message: types.Message, db: SQLite_db, user_info: UserData):
    results = db.checkall(
        GET_SEARCH_RESULT_REQ,
        [user_info.sex_partner, user_info.age_partner_from, user_info.age_partner_to, user_info.id]
    )
    if not results:
        results = db.checkall(GET_ALTER_SEARCH_RESULT_REQ, [user_info.id])
    if not results:
        return

    results = [db.to_model(i, UserData) for i in results]
    love = random.choice(results)
    db.query(ADD_PARTNER_REQ, [love.id, user_info.id])
    await message.answer('Собеседник найден')
    print(db.check('SELECT meeting_id FROM users WHERE id = ?', [user_info.id]))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
