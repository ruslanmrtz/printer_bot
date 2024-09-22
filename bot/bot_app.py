import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import user_handlers
from config import BOT_TOKEN

from bot import bot_db

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Инициализируем бот и диспетчер
bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
dp = Dispatcher(storage=storage)


# Настраиваем планировщик
scheduler = AsyncIOScheduler()
def start_scheduler():
    # Добавляем задание, которое будет выполняться каждые 60 секунд
    scheduler.add_job(user_handlers.check_expired_products, 'interval', seconds=60, args=[bot])
    scheduler.start()


# Функция конфигурирования и запуска бота
async def main():
    async with bot_db.engine.begin() as conn:
        await conn.run_sync(bot_db.Base.metadata.create_all)  # Создание таблиц

    start_scheduler()

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
