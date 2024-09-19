from config import BOT_TOKEN

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import user_handlers


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


# Функция конфигурирования и запуска бота
async def main():
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
