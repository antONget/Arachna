from aiogram import F, Router, Bot

from handlers.invite_handlers import process_start_callback_with_check_located_avatar
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import (list_storage_wardrobe_gun as LSWG,
                                list_storage_trash, list_storage_wardrobe, list_storage_gun,
                                LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_ALL_THINGS as All_Th,
                                dict_use_storage_trash as dict_u,
                                )
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf
import asyncio
from database.help_function import Backpack
from datetime import time, date, datetime, timedelta


router = Router()

storage = MemoryStorage()

import logging

class LaboratoryFSM(StatesGroup):
    state_save_lb4 = State()

#rlc1
@router.callback_query(F.data == 'relocate')
@router.callback_query(F.data == 'relocate!landing_place')
@router.callback_query(F.data == 'relocate!location_meadows')
async def rlc1(clb: CallbackQuery,  bot: Bot):
    tg_id=clb.message.chat.id
    logging.info(f"rlc1 --- clb.data = {clb.data}")

    if 'landing_place' in clb.data or 'location_meadows' in clb.data: # для возвращения обратно
        location = clb.data.split("!")[-1]
        # прийти обратно в текущую локацию можно через время, которое было потрачено на ходьбу
        # в БД записано время, когда начали движение
        time_begin_go = (await rq.get_user_dict(tg_id))['time'] # теперь +15 минут
        time_now = datetime.now()
        # текущее время - время когда прийду (+15) - 15 минут => сколько идти обратно                        ### = 15
        delta_time_to_go = time_now - (datetime.strptime(time_begin_go, '%Y-%m-%d %H:%M:%S.%f') - timedelta(minutes=1)) # 2025-01-10 15:13:22.705068 '%Y/%m/%d'
        seconds_to_go_back = int(delta_time_to_go.total_seconds())
        logging.info(f'delta_time = {delta_time_to_go} --- location = {location} --- total_seconds = {seconds_to_go_back}')
        # Запись в БД новой локации
        await rq.set_user(tg_id, 'location', location)
        # Зануляем время в строке time
        await rq.set_user(tg_id, 'time', 0)
        #if location == 'landing_place':
        #    photo = ph['location_meadows']
        #elif location == 'location_meadows':
        #    photo = ph['landing_place']
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[location]))
        await clb.message.edit_caption(caption=f"Вы вернетесь в локацию {All_Th[location]} через {seconds_to_go_back} секунд(у).")
        await asyncio.sleep(seconds_to_go_back)

    else:
        data_user = await rq.get_user_dict(tg_id)
        location = data_user['location']

    if location == 'landing_place':
        dict_kb = {'Бескрайние луга': 'relocate_location', 'Назад': 'checking_where_avatar_is_located'}
    elif location == 'location_meadows':
        dict_kb = {'Место посадки': 'relocate_location', 'Назад': 'checking_where_avatar_is_located'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    if location == 'landing_place':
        photo = ph['location_meadows']
    elif location == 'location_meadows':
        photo = ph['landing_place']
    await clb.message.edit_media(media=InputMediaPhoto(media=photo))
    await clb.message.edit_caption(caption=f"Куда хотите переместиться", reply_markup=keyboard)
    #await clb.answer()


#rlc2
@router.callback_query(F.data == 'relocate_location')
async def rlc2(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"rlc2 --- clb.data = {clb.data}")

    dict_kb = {'в путь!': 'relocate_location_start', 'Назад': 'relocate'}
    keyboard = kb.create_in_kb(1, **dict_kb)
  #  await clb.message.edit_media(media=InputMediaPhoto(media=ph['N20']))
    await clb.message.edit_caption(caption=f"Время в пути займет 15 минут.\n В РЕЖИМЕ ТЕСТИРОВАНИЯ ЧЕРЕЗ 1 МУНУТУ", reply_markup=keyboard)###


#rlc3
@router.callback_query(F.data == 'relocate_location_start')
async def rlc3(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"rlc3 --- clb.data = {clb.data}")

    dict_kb = {'ok': 'location_go_to'}
    keyboard = kb.create_in_kb(1, **dict_kb)
   # await clb.message.edit_media(media=InputMediaPhoto(media=ph['N20']))
    await clb.message.edit_caption(caption=f"Вы отправились в путь.", reply_markup=keyboard)


#rlc4
@router.callback_query(F.data == 'location_go_to')
@router.callback_query(F.data == 'location_go_to_back')
async def rlc4(clb: CallbackQuery, bot: Bot, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"rlc4 --- clb.data = {clb.data}")

    if clb.data == 'location_go_to':
        time_now = datetime.now()
        time = datetime.now() + timedelta(minutes=1)###5) #  В режиме тестирования одну минуту
        str_time = time.strftime('%H:%M')
        ###
        # в БД в таблицу user заносится этот time_now ВРЕМЯ без добавки 15 минут в БД
        await rq.set_user(tg_id=tg_id, name_column='time', current_value=time)
        # записать в переменную location актуальную локацию
        location = (await rq.get_user_dict(tg_id))['location']

        # для пояснения в какую локацию идем в переменную location_to_go записываем противоположную локацию от текущей из БД
        # и прибавляем к go_to! в колбэке
        if location == 'landing_place':
            location_to_go = 'location_meadows'
        elif location == 'location_meadows':
            location_to_go = 'landing_place'
        # перезапись локации на go_to!{location_to_go}
        await rq.set_user(tg_id=tg_id, name_column='location', current_value=f'go_to!{location_to_go}') #go_to!landing_place

    else:
        time = datetime.strptime((await rq.get_user_dict(tg_id))['time'], '%Y-%m-%d %H:%M:%S.%f')
        str_time = time.strftime('%H:%M')
        current_location = (await rq.get_user_dict(tg_id))['location'].split('!')[-1]

        if current_location == 'landing_place':
            location = 'location_meadows'
        elif current_location == 'location_meadows':
            location = 'landing_place'

    # go_to сделана для того, чтобы при нажатии "Назад" в рюкзаке или Характеристиках переходили на локацию "В пути"
    dict_kb={'Характеристики': 'specifications_go_to', 'Рюкзак': 'backpack_go_to',
                    'Вернуться': f'relocate!{location}', 'Выйти': 'checking_where_avatar_is_located'}
    keyboard = kb.create_in_kb(2, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Локация В пути.\n\nВы прибудете к месту назначения в {str_time}", reply_markup=keyboard)

    # установка отложенного запуска перехода в новую локацию
    await asyncio.sleep(60)#60 * 15) ### время в секундах

    ### проверка какая локация (go_to!...) и сколько прошло времени

    if 'go_to' in (await rq.get_user_dict(tg_id))['location']:
        # Запись в БД новой локации
        await rq.set_user(tg_id, 'location', location_to_go)
        # Зануляем время в строке time
        await rq.set_user(tg_id, 'time', 0)
        # Запускаем функцию которая и перекинет на проверку где аватар и
        await process_start_callback_with_check_located_avatar(clb, bot, state)
