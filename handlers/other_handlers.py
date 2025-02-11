from aiogram import Router, Bot
from aiogram.types import Message
import database.requests as rq


router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message, bot: Bot):
    tg_id = message.chat.id
    if message.text == 'add_backpack':
        await rq.set_storage_wardrobe(tg_id, 'backpack_foliage', '100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'backpack_leana', '100!1!1!2!3')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    #await message.answer(text=f'❌ <b>Неизвестная команда!</b>\n\n'
     #                    f'<i>Вы отправили сообщение напрямую в чат бота,</i>\n'
      #                   f'<i>или структура меню была изменена Админом.</i>\n\n'
       #                  f'ℹ️ Не отправляйте прямых сообщений боту\n'
        #                 f'или шуруйте в начало, нажав /start')
    if message.video:
        print(message.video.file_id)
    if message.photo:
        print(message.photo[-1].file_id)
