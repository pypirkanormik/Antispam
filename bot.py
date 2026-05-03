import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta

# ВАШ ТОКЕН
TOKEN = '8562869827:AAFEEkHDYJFbFm35sqLrVIcbIRWod8VUHig'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_last_time = {}

# Реагируем на любой контент: текст, стикеры, видео и т.д.
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def anti_flood_handler(message: types.Message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    last_time = user_last_time.get(user_id, 0)
    # Интервал 1.5 секунды между любыми сообщениями/стикерами
    is_flood = (current_time - last_time) < 1.5
    user_last_time[user_id] = current_time

    if is_flood:
        try:
            # 1. Удаляем флуд (сообщение или стикер)
            await message.delete()

            # 2. Устанавливаем мут на 5 минут
            mute_duration = 5
            until_date = datetime.now() + timedelta(minutes=mute_duration)
            
            await bot.restrict_chat_member(
                chat_id,
                user_id,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_other_messages=False, # Блокирует стикеры/ГП
                    can_send_polls=False
                ),
                until_date=until_date
            )

            # 3. Отправляем отчет
            report_text = (
                f"🚫 {message.from_user.full_name}, спам запрещен!\n"
                f"⏳ Вы замучены на **{mute_duration} минут**.\n"
                f"🔓 Разблокировка: {(datetime.now() + timedelta(minutes=mute_duration)).strftime('%H:%M:%S')}"
            )
            
            report = await message.answer(report_text, parse_mode="Markdown")
            
            # 4. Удаляем отчет бота через 15 секунд
            await asyncio.sleep(15)
            await report.delete()

        except Exception as e:
            logging.error(f"Ошибка при наказании: {e}")

async def main():
    print("Бот запущен. Мут на 5 минут активен для всех (включая стикеры).")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
