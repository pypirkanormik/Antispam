import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta

# ТОКЕН
TOKEN = '8562869827:AAFEEkHDYJFbFm35sqLrVIcbIRWod8VUHig'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_last_time = {}

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def anti_flood_handler(message: types.Message):
    if not message.from_user:
        return

    # ТЕСТ: Печатаем в консоль лог
    print(f"[{message.chat.title}] {message.from_user.full_name}: {message.text}")

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    last_time = user_last_time.get(user_id, 0)
    is_flood = (current_time - last_time) < 1.5
    user_last_time[user_id] = current_time

    if is_flood:
        try:
            # Проверяем статус пользователя
            member = await bot.get_chat_member(chat_id, user_id)
            
            # Если пользователь — не админ и не создатель, применяем санкции
            if member.status not in ["creator", "administrator"]:
                await message.delete()
                # Ограничиваем на 1 минуту (mute)
                until_date = datetime.now() + timedelta(minutes=1)
                await bot.restrict_chat_member(
                    chat_id, 
                    user_id, 
                    permissions=types.ChatPermissions(can_send_messages=False),
                    until_date=until_date
                )
                print(f"Пользователь {user_id} замучен за флуд.")
        except Exception as e:
            print(f"Ошибка при обработке флуда: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
