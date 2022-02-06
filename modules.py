import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DB import SQLite_db
from middleware import Middleware

loop = asyncio.get_event_loop()
bot = Bot(token="", loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
db = SQLite_db('database.db')
dp.middleware.setup(Middleware(db))
