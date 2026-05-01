import asyncio
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta

# --- БЛОК ДЛЯ RENDER (чтобы бот не отключался) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()
# -------------------------------------------------

TOKEN = '8793483381:AAG-E46OI4n6GGOyZnv4iliunr7ixh3DVPA'

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_last_time = {}

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def anti_flood_handler(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()
    
    last_time = user_last_time.get(user_id, 0)
    is_flood = (current_time - last_time) < 1.5

    if is_flood:
        try:
            await message.delete()
            member = await bot.get_chat_member(chat_id, user_id)
            
            if member.status not in ["creator", "administrator"]:
                until_date = datetime.now() + timedelta(minutes=5)
                await bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=types.ChatPermissions(can_send_messages=False),
                    until_date=until_date
                )
                await message.answer(f"🤫 @{message.from_user.username} в муте на 5 мин за флуд.")
            else:
                warn = await message.answer(f"⚠️ Админ @{message.from_user.username}, не флуди!")
                await asyncio.sleep(3)
                await warn.delete()
                
        except Exception as e:
            print(f"Ошибка: {e}")
        return

    user_last_time[user_id] = current_time

async def main():
    print("Бот-антифлуд запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
