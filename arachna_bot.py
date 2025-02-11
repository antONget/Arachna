import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import invite_handlers, other_handlers
from handlers.location_landing_place_h import (laboratory, location, dispose_of, repair,
                                               st_trash, st_trash_use_throw, bio, wardrobe, gun
                                               )
from handlers.location_anather_h import (relocate, meadows_loot, meadows_hunt)
from handlers.backpack_handlers import backpack
from handlers.invite_handlers import storage
from handlers.specifications import (specifications)
from database.models import async_main
from aiogram.types import ErrorEvent
import traceback
from aiogram.types import FSInputFile

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    await async_main()

   # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    # Регистриуем роутеры в диспетчере
    dp.include_router(invite_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(location.router)
    dp.include_router(backpack.router)
    dp.include_router(laboratory.router)
    dp.include_router(dispose_of.router)
    dp.include_router(repair.router)
    dp.include_router(st_trash.router)
    dp.include_router(st_trash_use_throw.router)
    dp.include_router(bio.router)
    dp.include_router(wardrobe.router)
    dp.include_router(specifications.router)
    dp.include_router(gun.router)
    dp.include_router(relocate.router)
    dp.include_router(meadows_loot.router)
    dp.include_router(meadows_hunt.router)

    @dp.error()
    async def error_handler(event: ErrorEvent):
        logger.critical("Критическая ошибка: %s", event.exception, exc_info=True)
        await bot.send_message(chat_id=config.tg_bot.support_id,
                               text=f'{event.exception}')
        formatted_lines = traceback.format_exc()
        text_file = open('error.txt', 'w')
        text_file.write(str(formatted_lines))
        text_file.close()
        await bot.send_document(chat_id=config.tg_bot.support_id,
                                document=FSInputFile('error.txt'))


    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())