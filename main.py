import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router, notifier

load_dotenv()
TOKEN = getenv("BOT_TOKEN")




async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.create_task(notifier(bot))
    
    # Підключаємо твій роутер з усіма командами
    dp.include_router(router)
    
    # Запускаємо бота
    print("Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())