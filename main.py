import asyncio
from bot import bot, dp


async def main():
    #await bot.delete_webhook(drop_pending_updates=True)
    #await dp.start_polling(bot)

    try:
        # Delete webhook (in case it was previously set) and start polling
        await bot.delete_webhook(drop_pending_updates=True)
    finally:
        await bot.session.close()
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
