import asyncio
from telegram import Bot

# Reemplaza 'YOUR_BOT_TOKEN' con el token que obtuviste de BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Reemplaza 'YOUR_CHAT_ID' con el ID de tu chat (o grupo) donde quieres enviar el mensaje
CHAT_ID = 'YOUR_CHAT_ID'

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Hola mundo 👋")

asyncio.run(main())
