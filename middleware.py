from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from DB import SQLite_db


class Middleware(BaseMiddleware):
    def __init__(self, db: SQLite_db):
        self.db = db
        self.req = 'SELECT id, sex, name, age, partner FROM users WHERE id = ?'

        super(Middleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['db'] = self.db
        u = self.db.check(self.req, [message.from_user.id])

        data['user_info'] = u
        data['partner_info'] = self.db.check(self.req, [u[4]]) if u and u[4] else None

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['db'] = self.db
        u = self.db.check(self.req, [callback_query.from_user.id])

        data['user_info'] = u
        data['partner_info'] = self.db.check(self.req, [u[4]]) if u and u[4] else None