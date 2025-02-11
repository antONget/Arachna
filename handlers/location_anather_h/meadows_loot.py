from aiogram import F, Router, Bot


from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import (list_storage_wardrobe_gun as LSWG,
                                list_storage_trash, list_storage_wardrobe, list_storage_gun,
                                LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_ALL_THINGS as All_Th,
                                dict_use_storage_trash as dict_u, LEXICON_scribe_trash as LScrTr,

                                )
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf
from database.help_function import Backpack
from datetime import datetime, timedelta
import random, asyncio


router = Router()

storage = MemoryStorage()

import logging

#class MeadowsLootFSM(StatesGroup):
 #   state_meadows1 = State() # F.data == 'location_meadows'
  #  state_loot_2 = State() # F.data == 'loot2'

@router.callback_query(F.data == 'location_meadows')
async def meadows1(clb: CallbackQuery, state = FSMContext):
    logging.info(f"meadows1 --- clb.data = {clb.data}")
    #logging.info(f'\n СЛЕДУЮЩЕЙ СТРОКОЙ ИДЕТ ЧИСТКА СОСТОЯНИЯ    state.get_state() = {await state.get_state()} ------ state.get_data() = {await state.get_data()}')
    await state.clear()
  #  await state.set_state(MeadowsLootFSM.state_meadows1)

    dict_kb={'Характеристики': 'specifications_meadows', 'Рюкзак': 'backpack_meadows',
            'Переместиться': 'relocate', 'Локация': 'location_meadows_start',
            'Выйти': 'checking_where_avatar_is_located'}

    keyboard = kb.create_in_kb(2, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N20']))
    await clb.message.edit_caption(caption=f"Локация Бескрайние луга", reply_markup=keyboard)
    #await clb.answer()



@router.callback_query(F.data == 'location_meadows_start')
async def meadows2(clb: CallbackQuery, state: FSMContext):
    #tg_id=clb.message.chat.id
    logging.info(f"meadows2 --- clb.data = {clb.data}")

    await state.clear()

    dict_kb={'Лут': 'loot', 'Охота': 'hunting',
            'Назад': 'location_meadows',}

    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Локация Бескрайние луга.", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'location_meadows_start')
async def meadows2(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"meadows2 --- clb.data = {clb.data}")

    dict_kb={'Лут': 'loot', 'Охота': 'hunting',
            'Назад': 'location_meadows',}

    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Локация Бескрайние луга.", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'loot')
async def loot(clb: CallbackQuery):
    tg_id=clb.message.chat.id
    logging.info(f"loot --- clb.data = {clb.data}")
    dict_kb={'Ok': 'loot1'}


    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Поиск займет от 1 до 5 минут.\n В РЕЖИМЕ ТЕСТИРОВАНИЯ 0 МИНУТ\n ", reply_markup=keyboard)
    minutes = 0 ###random.randint(1, 5)
    logging.info(f'minutes = {minutes}')
    current_time = datetime.now()
    await rq.set_user(tg_id, 'time', f'{current_time}!{minutes}')

    await asyncio.sleep(0)#60*minutes)
    # как пройдет время алерт с сообщением
    await clb.answer(
        text='Поиск завершен',
        show_alert=True
    )

    #await clb.answer()


@router.callback_query(F.data == 'loot1')
async def loot1(clb: CallbackQuery):
    logging.info(f"loot1 --- clb.data = {clb.data}")

    tg_id=clb.message.chat.id
    time_now = datetime.now()
    current_time_minutes = (await rq.get_user_dict(tg_id))['time']
    current_time = datetime.strptime(current_time_minutes.split('!')[0], '%Y-%m-%d %H:%M:%S.%f')
    minutes = int(current_time_minutes.split('!')[1])


    if time_now - timedelta(minutes=minutes) > current_time:
        clb_data_for_check = 'loot2'
    else:
        clb_data_for_check = 'loot1'
    dict_kb={'Проверить': clb_data_for_check, 'Выйти': 'st_0'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    try:
        await clb.message.edit_caption(caption=f"Поиск полезностей", reply_markup=keyboard)
    except:
        await clb.message.edit_caption(caption=f"Поиск полезностeй.", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'loot2')
async def loot2(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"loot2 --- clb.data = {clb.data}")

    # Для возвращения из Рюкзака именно в этот хэндлер сталю состояние,      ЧЕРЕЗ БД
    # которое удалю в хэндлере распихивания всего по рюкзаку
    #await state.set_state(MeadowsLootFSM.state_loot_2)
    dict_loot = await state.get_data()
    logging.info(f'dict_loot = {dict_loot}')
    if not dict_loot:
        berries = random.randint(2, 4)
        vine_leaves = random.randint(1, 2)
        yel_fl = random.randint(2, 6)
        stick = random.randint(2, 4)
        seed_zlg = 1
        dict_loot = {'berries': berries, 'vine_leaves': vine_leaves, 'yel_fl': yel_fl, 'stick': stick, 'seed_zlg': seed_zlg}
        await state.update_data(dict_loot)
    #else:
     #   dict_loot: dict = {}
      #  if dict_['berries']:
       #     #dict_loot.update({'berries': berries})
        #    berries = dict_['berries']
  #      if dict_['vine_leaves']:
   #         vine_leaves = dict_['vine_leaves']
    #    if dict_['yel_fl']:
     #       yel_fl = dict_['yel_fl']
      #  if dict_['stick']:
       #     stick = dict_['stick']
        #if dict_['seed_zlg']:
         #   seed_zlg = dict_['seed_zlg']


    #logging.info(f"'berries'= {berries}, 'vine_leaves' = {vine_leaves}, 'yel_fl' = {yel_fl}, 'stick' = {stick}, 'seed_zlg' = {seed_zlg}")
    #dict_loot = {'berries': berries, 'vine_leaves': vine_leaves, 'yel_fl': yel_fl, 'stick': stick, 'seed_zlg': seed_zlg}
    # проходим по словарю и если есть нулевые значения, добавляем этот ключ в список,
    # а потом проходим по этому списку и удаляем эти ключи из словаря
    list_with_zero_key: list = []
    for key, value in dict_loot.items():
        if value == 0:
            list_with_zero_key.append(key)
        #logging.info(f'list_with_zero_key = {list_with_zero_key}')
    if list_with_zero_key:
        for elem in list_with_zero_key:
            dict_loot.pop(elem)
        logging.info(f'dict_loot = {dict_loot}')
    #dict_kb={'Ягода вефиеры': 'descriptions!berries', f'{a} шт': f'what_do!berries!{a}',
     #        'Листья лозы': 'descriptions!vine_leaves', f'{b} шт': f'what_do!vine_leaves!{b}',
      #       'Стебель желтоцвета': 'descriptions!yel_fl',# f'{c} шт': f'what_do!yel_fl!{c}',
       #      'Палка': 'descriptions!stick',# f'{d} шт': f'what_do!stick!{d}',
        #     'Семечка злотоглавки': 'descriptions!seed_zlg',# '1 шт': 'what_do_seed!zlotoglavka!1',
         #    'взять всё': 'take_all_loot', 'рюкзак': 'backpack_loot',
          #   'не брать': 'do_not_take_loot'
           #  }
    #keyboard = kb.create_in_kb(2, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    keyboard = kb.create_list_in_kb(
        width=2,
        dict_=dict_loot,
        prefix1='descriptions!',
        prefix2='what_do!',
        backpack_clb_back='backpack_loot', # рюкзак
        take_all_='loot', # взять всё       take_all_' есть  в колбэке, чтобы не спутать с hunt
        do_not_take_='loot' # не брать      'do_not_take_' есть  в колбэке, чтобы не спутать с hunt
    )
    await clb.message.edit_caption(caption=f"Вы нашли", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data.startswith('descriptions!'))
async def loot3(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"loot3 --- clb.data = {clb.data}")
    name_loot = clb.data.split('!')[-1]
    if name_loot in ['luvron_polevoy', 'blue_rabbit', 'daron']:
        clb_back = 'hunting2_back'
    elif name_loot in ['raw_meat', 'bones', 'veins']:
        clb_back = 'you_are_win'
    else:
        clb_back = 'loot2'
    dict_kb={'Назад': clb_back,}
    keyboard = kb.create_in_kb(1, **dict_kb)
    #### имя картинки
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_loot]))
    await clb.message.edit_caption(caption=f"{LScrTr[name_loot]}", reply_markup=keyboard)
    #await clb.answer()

#loot_pb!berries!backpack_leana!r!X!3!cell_3
#loot_pb!backpack_leana!r!X!3!cell_2

@router.callback_query(F.data.startswith('what_do!'))
async def loot4(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"loot4 --- clb.data = {clb.data}")
    name_loot = clb.data.split('!')[-2]
    number_loot = clb.data.split('!')[-1]
    dict_kb={'Положить в рюкзак': f'put_on_backpack_loot!{name_loot}!{number_loot}',
             'Использовать': f'use_loot!{name_loot}!{number_loot}',
             'Назад': 'loot2',
             }
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_loot]))
    await clb.message.edit_caption(caption=f"Что делаем с {All_Th[name_loot.upper()]} {number_loot} шт", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data.startswith('use_loot!'))
async def use_loot(clb: CallbackQuery):
    tg_id=clb.message.chat.id
    logging.info(f"use_loot --- clb.data = {clb.data}")
    data_ = (await rq.get_user_dict(tg_id))['xp']
    name_loot = clb.data.split('!')[-2]
    number_loot = clb.data.split('!')[-1]
    dict_kb = {'Использовать': f'use_loot_end!{name_loot}!{number_loot}', 'Назад': f'what_do!{name_loot}!{number_loot}',}
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_loot]))

    if name_loot in dict_u:
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_caption(caption=f"Вы хотите использовать {LST[name_loot.capitalize()]} \n"
                                        f"{LST[name_loot]} восстановит до {dict_u[name_loot]}ХП \n"
                                        f"У вас {data_}ХП, максимально 100ХП", reply_markup=keyboard)
    else:
        keyboard = kb.create_in_kb(1, **{'ok': f'what_do!{name_loot}!{number_loot}'})
        await clb.message.edit_caption(caption=f"Только лекарство можно обменять на ХП.\n"
                                        f"{All_Th[name_loot]} не лекарство",
                                        reply_markup=keyboard)
    await clb.answer()


@router.callback_query(F.data.startswith('use_loot_end!'))
async def use_loot_end(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"use_loot_end --- clb.data = {clb.data}")

    name_loot = clb.data.split('!')[-2]
    number_loot = clb.data.split('!')[-1]


    value_xp = (await rq.get_user_dict(tg_id=tg_id))['xp']

    if value_xp < 100 - int(dict_u[name_loot]):
        value_xp+=int(dict_u[name_loot])
    else:
        value_xp = 100

    await rq.set_user_xp(tg_id=tg_id, current_xp=value_xp)

    dict_ = await state.get_data()
    logging.info(f'dict_ = {dict_}')
    if dict_['berries']>0:
        await state.update_data({'berries': dict_['berries']-1})
    elif dict_['berries']==0:
        dict_.pop('berries')
        await state.clear()
        await state.update_data(dict_)

    keyboard = kb.create_in_kb(1, **{LBut['ok']: 'loot2'})
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_loot]))

    await clb.message.edit_caption(caption=f"Вы использовали {LST[name_loot.capitalize()]} 1 шт.\n"
                                    f"Осталось {dict_['berries']-1} шт. \n"
                                    f"У вас {value_xp} ХП", reply_markup=keyboard)

    await clb.answer()




@router.callback_query(F.data == 'take_all_loot')
@router.callback_query(F.data == 'take_all_hunt')
async def take_all_loot(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"take_all_loot\hunt --- clb.data = {clb.data}")

    if clb.data.startswith('take_all_loot'):
        clb_back = 'loot2'

    elif clb.data.startswith('take_all_hunt'):
        clb_back = 'you_are_win'


    # какой лут есть (остался) в словаре из состояния
    #dict_loot = await state.get_data()
    # функция проверяет может ли вместиться лут в надетый рюкзак, если да, то перемещает
    #check_all_loot = await hf.check_all_loot_put_on_pockets_and_cells_backpack_if_yes_remove(
    #    tg_id=tg_id,
    #    dict_loot=dict_loot)

    #await hf.create_list_with_dict_all_things_from_pocket_and_cell_backpack(tg_id=tg_id)
    keyboard = kb.create_in_kb(1, **{'ok': clb_back})
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
    await clb.message.edit_caption(caption="Весь этот лут в рюкзак не вмещается", reply_markup=keyboard)
    #await clb.message.edit_caption(caption="Эта часть программы в разработке", reply_markup=keyboard)
    #await clb.message.edit_caption(caption="Вы положили все в рюкзак", reply_markup=keyboard)
    ###await state.clear() # очистка словаря с найденным лутом
    await clb.answer()

    #    keyboard = kb.create_in_kb(1, **{'ok': 'loot2'})
     #   await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
      #  await clb.message.edit_caption(caption="Весь этот лут в рюкзак не вмещается", reply_markup=keyboard)
       # await clb.answer()



@router.callback_query(F.data.startswith('put_on_backpack_loot'))
@router.callback_query(F.data.startswith('put_on_backpack_hunt'))
async def put_on_backpack_loot(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"put_on_backpack_loot --- clb.data = {clb.data}")
# ПОЛОЖИТЬ В РЮКЗАК
# 'Положить в рюкзак': f'put_on_backpack_loot!{name_loot}!{number_loot}',
    clb_name = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]

    if clb.data.startswith('put_on_backpack_loot'):
        what_do = 'what_do'
        loot_pb = "loot_pb"
    elif clb.data.startswith('put_on_backpack_hunt'):
        what_do = 'what_do_hunt'
        loot_pb = "loot_pb_h"
    backpack = await hf.what_backpack_put_on(tg_id=tg_id)
    # если никакой, то сообщение, что рюкзака нет
    #logging.info(f'name_value_user = {name_value_user}')
    if backpack == 'no_backpack': # если рюкзак не надет
        #keyboard = kb.create_in_kb(1, **{'Ok': f'{what_do}!{clb_name}!{clb_value}'}) # +
        #await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        #await clb.message.edit_caption(caption=f"Рюкзак не надет. Класть некуда.", reply_markup=keyboard)
        #await clb.answer()

        list_cell = await hf.create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell(
            tg_id=tg_id, value_pocket_cell=clb_value, clb_name=clb_name, prefix=loot_pb)#, backpack=backpack) # +
        # Пишу функцию, которая из БД делает список list_cell
       # keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back=f"put_on_backpack_loot!{clb_name}!{clb_value}")
        keyboard = kb.create_keyboard_from_colored_cell(
            list_pocket=list_cell[0],
            #list_cell=list_cell[1],
            clb_back=f"{what_do}!{clb_name}!{clb_value}")
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"Рюкзак не надет. \nДоступны только карманы.\nВ какую ячейку кладем?", reply_markup=keyboard)
        await clb.answer()

    elif backpack in ('backpack_foliage', 'backpack_leana'): # если надет какой-то рюкзак

        #if not await hf.check_xp_put_on_backpack_if_more_then_zero(tg_id=tg_id): # проваливаемся сюда, если ХП < 0
            # если ХП рюкзака меньше 0, то запускаю функцию  xp_backpack_is_over_remove_things_delate_backpack
        #    await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=backpack)
        #    return
        #await rq.decrease_xp_put_on_backpack_1(tg_id=tg_id) # уменьшаем ХП, если нажали на рюкзак и ХП > 0

        list_cell = await hf.create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell(
            tg_id=tg_id, value_pocket_cell=clb_value, clb_name=clb_name, prefix=loot_pb, backpack=backpack) # +
        # Пишу функцию, которая из БД делает список list_cell
       # keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back=f"put_on_backpack_loot!{clb_name}!{clb_value}")
        keyboard = kb.create_keyboard_from_colored_cell(
            list_pocket=list_cell[0],
            list_cell=list_cell[1],
            clb_back=f"{what_do}!{clb_name}!{clb_value}")
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"В какую ячейку кладем?", reply_markup=keyboard)
        await clb.answer()


@router.callback_query(F.data.startswith('loot_pb'))
async def loot_pb(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"loot_pb --- clb.data = {clb.data}")

# ['🟩', 'loot_pb!berries!backpack_leana!g!X!3!pocket1']
    clb_name = clb.data.split('!')[-6]
    clb_backpack = clb.data.split('!')[-5]
    clb_color_to_pc = clb.data.split('!')[-4]
    clb_value= clb.data.split('!')[-2]
    clb_to_pc = clb.data.split('!')[-1]

    if clb.data.startswith('loot_pb'):
        clb_back = 'loot2'
        prefix='loot_end'
    elif clb.data.startswith('loot_pb_h'):
        clb_back = 'you_are_win'
        prefix='loot_end_hunt'


    if clb_to_pc.startswith('cell'):
        if not await hf.check_xp_put_on_backpack_if_more_then_zero(tg_id=tg_id): # проваливаемся сюда, если ХП < 0
            # если ХП рюкзака меньше 0, то запускаю функцию  xp_backpack_is_over_remove_things_delate_backpack
            await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=clb_backpack)
            return
        await rq.decrease_xp_put_on_backpack_1(tg_id=tg_id) # уменьшаем ХП, если нажали на рюкзак и ХП > 0

    if clb_color_to_pc == 'r':
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            keyboard = kb.create_in_kb(1, **{'Назад': f'what_do!{clb_name}!{clb_value}'})
            await clb.message.edit_caption(caption=f"Сюда положить нельзя", reply_markup=keyboard)
    elif clb_color_to_pc in ['y', 'g']:
        value_to_pc = (await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(
                tg_id=tg_id,
                backpack=clb_backpack,
                pocket_cell=clb_to_pc))[1]

        keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(
                        tg_id=tg_id,
                        prefix=prefix,
                        value_pocket_cell=int(value_to_pc), # сколько лежит в выбранной ячейке
                        value_storage=int(clb_value), # сколько я налутовал?
                        clb_action='dologit',
                        clb_backpack=clb_backpack,
                        clb_pocket_cell=clb_to_pc,
                        clb_name=clb_name,
                        clb_back=clb_back
                        )

        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))

        await clb.message.edit_caption(
            caption=
            f"У вас есть {All_Th[clb_name]} {clb_value} шт.\n"
            f"Сколько хотите положить в {LBut[clb_to_pc.upper()]}?",
            reply_markup=keyboard)


@router.callback_query(F.data.startswith('loot_end'))
async def loot_end(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"loot_end --- clb.data = {clb.data}")
    # loot_end!2!dologit!backpack_leana!cell_4!berries!0


    clb_value_loot = int(clb.data.split('!')[-6])
    clb_bacpack = clb.data.split('!')[-4]
    clb_pocket_cell = clb.data.split('!')[-3]
    clb_name = clb.data.split('!')[-2]
    clb_value_pocket_cell = int(clb.data.split('!')[-1])

    if clb.data.startswith('loot_end'):
        clb_back = 'loot2'

    elif clb.data.startswith('loot_end_hunt'):
        clb_back = 'you_are_win'


    # если нажали кнопку "все", то переопределить из словаря состояния. Взять все луты
    dict_loot = await state.get_data()
    if clb_value_loot == 333:
        clb_value_loot = dict_loot[clb_name]

    # установка значения в рюкзак
    await hf.set_value_in_pocket_cell_put_on_backpack(
        tg_id=tg_id,
        backpack=clb_bacpack,
        pocket_cell=clb_pocket_cell,
        clb_name=clb_name,
        value = clb_value_loot + clb_value_pocket_cell
    )

    #dict_ = await state.get_data()
    #logging.info(f'dict_ = {dict_loot}')
    #if dict_loot['berries']>0:
    logging.info(f'\ndict_loot = {dict_loot}\n"clb_name" = {clb_name}')
    await state.update_data({clb_name: dict_loot[clb_name]-clb_value_loot})
    dict_loot = await state.get_data()
    if dict_loot[clb_name]==0:
        dict_loot.pop(clb_name)
        await state.clear()
        await state.update_data(dict_loot)

    dict_loot = await state.get_data()
    if dict_loot: # если в этом словаре еще что-то осталось

            #    dict_kb={'Положить в рюкзак': f'put_on_backpack_loot!{name_loot}!{number_loot}',
            keyboard = kb.create_in_kb(1, **{'ok': clb_back})
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(
                caption=f"Вы положили {All_Th[clb_name.capitalize()]}\n{clb_value_loot} шт.\nв {All_Th[clb_pocket_cell.upper()]}",
                reply_markup=keyboard)

    else:
        await state.clear()
        await meadows2(clb=clb)

        #keyboard = kb.create_list_in_kb(
        #width=2,
        #dict_=dict_loot,
        #prefix1='descriptions!',
        #prefix2='what_do!',
        #backpack_clb_back='backpack_loot', # рюкзак
        #take_all_loot='take_all_loot', # взять всё
        #do_not_take_loot='do_not_take_loot' # не брать
        #)
        #await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
        #await clb.message.edit_caption(caption=f"Вы нашли", reply_markup=keyboard)


# do_not_take_loot='do_not_take_loot' # не брать
@router.callback_query(F.data == 'do_not_take_loot')
@router.callback_query(F.data == 'do_not_take_hunt')
async def do_not_take_loot(clb: CallbackQuery, state: FSMContext):
    #tg_id=clb.message.chat.id
    logging.info(f"do_not_take_loot/hunt --- clb.data = {clb.data}")

    await state.clear()
    await meadows1(clb=clb, state=state)