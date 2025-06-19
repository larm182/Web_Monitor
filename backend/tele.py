import asyncio
from telegram import Bot

# Reemplaza 'YOUR_BOT_TOKEN' con el token que obtuviste de BotFather
TOKEN = '5562872839:AAGD06yp79PMg9OGy27_fgkVnlG7zKqM42s'

# Reemplaza 'YOUR_CHAT_ID' con el ID de tu chat (o grupo) donde quieres enviar el mensaje
CHAT_ID = '779516132'

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Hola mundo 👋")

asyncio.run(main())