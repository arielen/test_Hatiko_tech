import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from config import settings
from database.controllers import get_user_language, user_exists
from database.models import async_main
from handlers import router
from redis.asyncio import Redis


class CustomI18nMiddleware(SimpleI18nMiddleware):
    async def get_locale(self, event, data) -> str:
        user_id = data["event_from_user"].id
        if await user_exists(user_id):
            user_lang = await get_user_language(user_id)
            return user_lang.value if user_lang.value else self.default_locale
        return self.i18n.default_locale


async def main() -> None:
    await async_main()
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    i18n = I18n(path="bot/locales", default_locale="en", domain="messages")

    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    try:
        dp.include_router(router)
        dp.update.middleware(CustomI18nMiddleware(i18n))
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
    finally:
        await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
