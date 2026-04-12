import asyncio
from app.bot.dispatcher import bot, setup_dispatcher

async def main():
    dp = setup_dispatcher()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
