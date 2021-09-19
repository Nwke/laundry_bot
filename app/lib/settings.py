from os import getenv
from aiogram import Bot, Dispatcher, types
from sqlmodel import Session, create_engine, SQLModel
# Import database objects
from .db_objects import Laundry, Users

main_description = """
Привет, я помогу тебе упростить процесс стирки в общаге! 🤖
У меня есть два режима работы, сейчас я тебе о них расскажу.

1. Режим проверки стиралок ❔
Для этого тебе достаточно отправить мне команду /check и я покажу тебе, какие стиралки заняты или свободны.

2. Режим запуска стиралки 🧺
На 1 этаже стиральной комнаты расположены QR-коды, отсканировав которые можно запустить процесс стирки и сказать другим ребятам, что ты занял именно эту стиралку.

❗ Важное уточнение, все мы люди, а я робот, поэтому работоспособность данной системы лежит полностью на ваших плечах.

Удачного использования, надеюсь я смогу вам облегчить жизнь в этом плане😄
"""

TOKEN = getenv('TOKEN') or ''
ADMINS = list(map(int, (getenv('ADMINS') or '').split(',')))

# Setup aiogram
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)

# Setup sqlmodel
sqlite_file = 'db/databasse.db'
sqlite_url = f'sqlite:///{sqlite_file}'
connect_args = {
	"check_same_thread" : False
}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# Init machines
with Session(engine) as s:
	s.add(Laundry(machine="laundry_1"))
	s.add(Laundry(machine="laundry_2"))
	s.add(Laundry(machine="dryer"))

# Create database and tables
SQLModel.metadata.create_all(engine)