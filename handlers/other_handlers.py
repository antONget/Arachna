from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
import database.requests as rq

#gjgjggh
router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message, bot: Bot):
    tg_id = message.chat.id
    if message.text == '/add_backpack':
        await rq.set_storage_wardrobe(tg_id, 'backpack_foliage', '100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'backpack_leana', '100!1!1!2!3')
    if message.text == '/add_ trash':
        await rq.set_storage_trash(tg_id, 'f_aid', 100)
        await rq.set_storage_trash(tg_id, 'f_aid_s', 100)
        await rq.set_storage_trash(tg_id, 'bandages', 100)
        await rq.set_storage_trash(tg_id, 'bandages_s', 100)
        await rq.set_storage_trash(tg_id, 'canned_meat', 100)
        await rq.set_storage_trash(tg_id, 'fried_meat', 100)
        await rq.set_storage_trash(tg_id, 'fried_veins', 100)
        await rq.set_storage_trash(tg_id, 'berries', 100)
        await rq.set_storage_trash(tg_id, 'bones', 100)
        await rq.set_storage_trash(tg_id, 'veins', 100)
        await rq.set_storage_trash(tg_id, 'vine_leaves', 100)
        await rq.set_storage_trash(tg_id, 'yel_fl', 100)
        await rq.set_storage_trash(tg_id, 'stick', 100)
        await rq.set_storage_trash(tg_id, 'raw_meat', 100)
        await rq.set_storage_trash(tg_id, 'seed_zlg', 100)
    if message.text == '/add_ gun':
        await rq.set_storage_gun(tg_id, 'G17', '100!100!1!1!2!3')
        await rq.set_storage_gun(tg_id, 'spear', '100!100!1!1!2!3')
    if message.text == '/add_ armor':
        await rq.set_storage_wardrobe(tg_id, 'helmet_kosmonavt', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'helmet_wanderer', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'helmet_reinforced', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'dress_kosmonavt', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'dress_wanderer', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'dress_reinforced', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'shoes_kosmonavt', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'shoes_wanderer', '100!100!1!1!2!3')
        await rq.set_storage_wardrobe(tg_id, 'shoes_reinforced', '100!100!1!1!2!3')
    if message.text == '/add_ bio':
        await rq.set_storage_bio(tg_id, 'bio', 10000)
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
    if message.text == '/get_logfile':
        file_path = "py_log.log"
        await message.answer_document(FSInputFile(file_path))

    if message.text == '/get_DB':
        file_path = "database/db.sqlite3"
        await message.answer_document(FSInputFile(file_path))

