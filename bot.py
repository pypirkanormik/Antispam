import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta

TOKEN = '8793483381:AAG-E46OI4n6GGOyZnv4iliunr7ixh3DVPA'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для отслеживания времени последнего сообщения/стикера
user_last_time = {}

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def anti_flood_handler(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()
    
    last_time = user_last_time.get(user_id, 0)
    # Лимит времени между сообщениями/стикерами (1.5 секунды)
    is_flood = (current_time - last_time) < 1.5

    if is_flood:
        try:
            # Удаляем флуд (текст или стикер — не важно)
            await message.delete()

            member = await bot.get_chat_member(chat_id, user_id)
            
            if member.status not in ["creator", "administrator"]:
                # Мут на 5 минут за быструю отправку
                until_date = datetime.now() + timedelta(minutes=5)
                await bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=types.ChatPermissions(can_send_messages=False),
                    until_date=until_date
                )
                await message.answer(f"🤫 @{message.from_user.username} в муте на 5 мин за флуд.")
            else:
                # Админам просто чистим флуд без мута
                warn = await message.answer(f"⚠️ Админ @{message.from_user.username}, не флуди!")
                await asyncio.sleep(3)
                await warn.delete()
                
        except Exception as e:
            print(f"Ошибка: {e}")
        return

    # Если это не флуд, просто запоминаем время
    user_last_time[user_id] = current_time

async def main():
    print("Бот-антифлуд запущен! (Стикеры разрешены, если ими не спамить)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
