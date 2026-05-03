import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta

# НОВЫЙ ТОКЕН
TOKEN = '8562869827:AAFEEkHDYJFbFm35sqLrVIcbIRWod8VUHig'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_last_time = {}

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def anti_flood_handler(message: types.Message):
    # ТЕСТ: Печатаем в консоль всё, что видит бот
    print(f"[{message.chat.title}] {message.from_user.full_na>

    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    last_time = user_last_time.get(user_id, 0)
    is_flood = (current_time - last_time) < 1.5
    user_last_time[user_id] = current_time

    if is_flood:
        try:
            await message.delete()
            member = await bot.get_chat_member(chat_id, user_>

            if member.status not in ["creator", "administrato>
                until_date = datetime.now() + timedelta(minut>

^G Help     ^O Write Out^F Where Is ^K Cut      ^T Execute
^X Exit     ^R Read File^\ Replace  ^U Paste    ^J Justify
