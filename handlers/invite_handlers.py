from aiogram import F, Router, Bot

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import LEXICON_Invite as LI, LEXICON_BUTTON as LBut
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
from datetime import time, date, datetime, timedelta

router = Router()

storage = MemoryStorage()

import logging
import asyncio

#class InviteFSM(StatesGroup):
#    state_change_nickname = State()
  #  st_2 = State()
   # st_3 = State()


#@router.callback_query()
#async def process_start_(clb: CallbackQuery) -> None:

 #   logging.info(f'process_start --- {clb.message.message_id}')




# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message,  bot: Bot):
    logging.info(f'process_start_command')
    user_tg_id = [user.tg_id for user in await rq.get_users()]
    tg_id = message.chat.id
    # если id НЕТ в базе данных, то провести приветствие и записать в базу данных
    if message.chat.id not in user_tg_id: ### не забыть вернуть not

        keyboard = kb.create_in_kb(1, **{'Дальше': 'st_1'})

        await message.answer_photo(photo=ph['N5'], caption=LI['/start'], reply_markup=keyboard)
        #await message.answer(text=LI['/start'], reply_markup=keyboard)
        await bot.delete_message(chat_id=tg_id, message_id=message.message_id)

    #id ЕСТЬ в базе данных,=> переходим в состояние "проверка где аватар"
    else: # ВЫЗЫВАЙ СЛЕДУЮЩУЮ ФУНКЦИЮ!!! а как, там колбэк, а тут мессаджжж
        ### спрашивать у БД, в каком месте находится аватар и после этого отправлять его туда
        logging.info(f'process_start_command_with_regisration ---- {message.message_id}')
        data_user=await rq.get_user_dict(tg_id=tg_id)
        location = data_user['location']
        try:
            for i in range(1000):
                await bot.delete_message(chat_id=tg_id, message_id=message.message_id-i)
        except:
            pass

        if location == "landing_place":
            logging.info(f'location =="landing_place"')
            dict_kb={LBut['specifications']: 'specifications_lp', 'Рюкзак': 'backpack_landing_place',
                    'Переместиться': 'relocate', LBut['location']: 'location_landing_place',
                    LBut['cansel']: 'st_0',}
            keyboard = kb.create_in_kb(2, **dict_kb)
            await message.answer_photo(photo=ph['N5'], caption=LI['landing_place'], reply_markup=keyboard)
            #await message.answer(text=LI['landing_place'], reply_markup=keyboard)
            #await message.answer_photo()

        elif location == "location_meadows":
            logging.info(f'location =="location_meadows"')
            dict_kb={'Характеристики': 'specifications_meadows', 'Рюкзак': 'backpack_meadows',
                    'Переместиться': 'relocate', 'Локация': 'location_meadows_start',
                    'Выйти': 'st_0'}
            keyboard = kb.create_in_kb(2, **dict_kb)
            await message.answer_photo(photo=ph['N20'], caption='Локация Бескрайние луга', reply_markup=keyboard)


        elif 'go_to' in location:

            time_now = datetime.now()
            time_data_base = (await rq.get_user_dict(tg_id))['time']
            time_data_base = datetime.strptime(time_data_base, '%Y-%m-%d %H:%M:%S.%f')
            #minutes = int(current_time_minutes.split('!')[1])
            str_time = time_data_base.strftime('%H:%M')

            current_location = (await rq.get_user_dict(tg_id))['location'].split('!')[-1]
            if current_location == 'landing_place':
                location = 'location_meadows'
            elif current_location == 'location_meadows':
                location = 'landing_place'

            if time_now - time_data_base > timedelta(minutes=0):
                # время перехода вышло и можно показывать новую локацию

                # Запись в БД новой локации
                await rq.set_user(tg_id, 'location', location)
                # Зануляем время в строке time
                await rq.set_user(tg_id, 'time', 0)
                # Запускаем функцию которая и перекинет на проверку где аватар и
                await process_start_command(message, bot)
                #return

                #time = datetime.strptime((await rq.get_user_dict(tg_id))['time'], '%Y-%m-%d %H:%M:%S.%f')

            else:

            # go_to сделана для того, чтобы при нажатии "Назад" в рюкзаке или Характеристиках переходили на локацию "В пути"
                dict_kb={'Характеристики': 'specifications_go_to', 'Рюкзак': 'backpack_go_to',
                         'Вернуться': f'relocate!{location}', 'Выйти': 'checking_where_avatar_is_located'}
                keyboard = kb.create_in_kb(2, **dict_kb)
                await message.answer_photo(
                    photo=ph['N21'],
                    caption=f"Локация В пути.\n\nВы прибудете к месту назначения в {str_time}",
                    reply_markup=keyboard)



                new_delta_minutes_for_sleep = time_data_base - time_now
                new_delta_minutes_for_sleep = new_delta_minutes_for_sleep.seconds#int(new_delta_minutes_for_sleep.strftime('%M'))
                logging.info(f'new_delta_minutes_for_sleep = {new_delta_minutes_for_sleep}')


                # установка отложенного запуска перехода в новую локацию
                await asyncio.sleep(new_delta_minutes_for_sleep)#60*new_delta_minutes_for_sleep)#60 * 15) ### время в секундах
                await rq.set_user(tg_id, 'location', location)
                # Зануляем время в строке time
                await rq.set_user(tg_id, 'time', 0)
                # Запускаем функцию которая и перекинет на проверку где аватар и
                await process_start_command(message, bot)

            ### проверка какая локация (go_to!...) и сколько прошло времени



        ### здесь ещё две локации чере! при переходе записываются

        #elif location == "В пути"
        #elif location == "Луга"



@router.callback_query(F.data == 'start')
@router.callback_query(F.data == 'checking_where_avatar_is_located')
async def process_start_callback_with_check_located_avatar(clb: CallbackQuery,  bot: Bot, state: FSMContext) -> None:
    """
    Проверка где находится аватар
    :param callback:
    :param bot:
    :return:
    """
    user_tg_id = [user.tg_id for user in await rq.get_users()]
    logging.info('process_start_callback_with_check_located_avatar')
    tg_id = clb.message.chat.id

    await state.clear()

    if tg_id not in user_tg_id: ### не забыть вернуть not
        # приветствие
        logging.info('process_start_callback_with_check_located_avatar, if not registration')
        #await clb.message.answer_photo(photo=ph['N_1'])
        kb_d = {LBut['next']: 'st_1'}
        keyboard = kb.create_in_kb(1, **kb_d)
        #await clb.message.answer(text=LI['/start'], reply_markup=keyboard)
        #await bot.delete_message(chat_id=tg_id, message_id=clb.message.message_id)
        #await clb.message.answer_photo(photo=ph['N5'], caption=LI['/start'], reply_markup=keyboard)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N5']))
        await clb.message.edit_caption(caption=LI['/start'], reply_markup=keyboard)
        await clb.answer()
    else:
        logging.info('process_start_callback_with_check_located_avatar with registration')
        try:
            await bot.delete_message(chat_id=tg_id, message_id=clb.message.message_id-1)
        except:
            pass
        data_table_user=await rq.get_user_dict(tg_id=tg_id)
        location = data_table_user['location']

        if location == "landing_place":
            dict_kb={'Характеристики': 'specifications_lp', 'Рюкзак': 'backpack_landing_place',
                    'Переместиться': 'relocate', 'Локация': 'location_landing_place',
                    'Выйти': 'st_0',}
            keyboard = kb.create_in_kb(2, **dict_kb)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N5']))
            await clb.message.edit_caption(caption=LI['landing_place'], reply_markup=keyboard)
            await clb.answer()

        elif location == "location_meadows":
            logging.info(f'location =="location_meadows"')
            dict_kb={'Характеристики': 'specifications_meadows', 'Рюкзак': 'backpack_meadows',
                    'Переместиться': 'relocate', 'Локация': 'location_meadows_start',
                    'Выйти': 'st_0'}

            keyboard = kb.create_in_kb(2, **dict_kb)
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N20']))
            await clb.message.edit_caption(caption=f"Локация Бескрайние луга", reply_markup=keyboard)

        #elif location == "В пути"







@router.callback_query(F.data == 'st_1')
async def process_st_1(clb: CallbackQuery, bot: Bot):
    logging.info(f'process_st_1: {clb.message.chat.id}')
    tg_id = clb.message.chat.id
    #try:
     #   await bot.delete_message(chat_id=)
    keyboard = kb.create_in_kb(1, **{'Дальше': 'st_2'})

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N1']))
    await clb.message.edit_caption(caption=LI['st_1'], reply_markup=keyboard)

   # await bot.delete_message(chat_id=tg_id, message_id=clb.message.message_id)
    #await bot.edit_message_media(media=InputMediaPhoto(media=ph['N_1']))# caption=LI['st_1'], reply_markup=keyboard)

    #await clb.message.answer_photo(photo=ph['N_1'], caption=LI['st_1'], reply_markup=keyboard)
    #await clb.message.edit_media(media=InputMediaPhoto(media=ph['N_1']))
    #await clb.message.answer(text=LI['st_1'], reply_markup=keyboard)


@router.callback_query(F.data == 'st_2')
async def process_st_2(clb: CallbackQuery, bot: Bot):
    logging.info(f'process_st_2')
    #await callback.message.answer_photo(photo=ph['N_2'])
    keyboard = kb.create_in_kb(1, **{LBut['next']: 'st_3'})
    #await callback.message.answer(text=LI['st_2'], reply_markup=keyboard)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N2']))
    await clb.message.edit_caption(caption=LI['st_2'], reply_markup=keyboard)


@router.callback_query(F.data == 'st_3')
async def process_st_3(clb: CallbackQuery, bot: Bot):
    logging.info(f'process_st_3')

    kwards = {LBut['register']: 'st_4', LBut['cansel']:  'st_0'}
    keyboard = kb.create_in_kb(1, **kwards)
    #await callback.message.answer(text=LI['st_3'], reply_markup=keyboard)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N3']))
    await clb.message.edit_caption(caption=LI['st_3'], reply_markup=keyboard)


@router.callback_query(F.data == 'st_4')
async def process_st_4(clb: CallbackQuery, bot: Bot):
    logging.info(f'process_st_4')

    keyboard = kb.create_in_kb(1, **{LBut['next']: 'st_5'})
    #await callback.message.answer(text=LI['st_4'], reply_markup=keyboard)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N4']))
    await clb.message.edit_caption(caption=LI['st_4'], reply_markup=keyboard)

    #добавление id нового пользователя в БД
    dict_tg_id = {'tg_id': clb.message.chat.id,
                  'name_user': clb.message.chat.first_name,}
    await rq.add_new_user(data=dict_tg_id)

@router.callback_query(F.data == 'st_5')
async def process_st_5(clb: CallbackQuery, bot: Bot):
    logging.info(f'process_st_5')

    keyboard = kb.create_in_kb(1, **{LBut['begin_start']: 'start'})
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N5']))
    await clb.message.edit_caption(caption=LI['st_5'], reply_markup=keyboard)

    #await callback.message.answer(text=LI['st_5'], reply_markup=keyboard)

@router.callback_query(F.data == 'st_0')
async def process_st_0(clb: CallbackQuery):
    logging.info(f'process_st_0')

    dict_kb={LBut['begin_start']:'start'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N1']))
    await clb.message.edit_caption(caption='Для повторного запуска напишите /start или начать', reply_markup=keyboard)
