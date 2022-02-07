from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from DB import SQLite_db
from models import UserData


class Middleware(BaseMiddleware):
    def __init__(self, db: SQLite_db):
        self.db = db
        self.req = 'SELECT id, sex, name, age, sex_partner, age_partner_from, age_partner_to, meeting_id ' \
                   'FROM users WHERE id = ?'

        super(Middleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['db'] = self.db

        u = self.db.check(self.req, [message.from_user.id])
        d_u = self.db.to_model(u, UserData)
        data['user_info'] = d_u

        pu = self.db.check(self.req, [d_u.meeting_id]) if d_u and d_u.meeting_id else None
        data['partner_info'] = self.db.to_model(pu, UserData) if pu else None

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['db'] = self.db

        u = self.db.check(self.req, [callback_query.from_user.id])
        d_u = self.db.to_model(u, UserData)
        data['user_info'] = d_u

        pu = self.db.check(self.req, [d_u.meeting_id]) if d_u and d_u.meeting_id else None
        data['partner_info'] = self.db.to_model(pu, UserData) if pu else None
