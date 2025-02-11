from aiogram import F, Router, Bot


from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import (list_storage_wardrobe_gun as LSWG,
                                list_storage_trash, list_storage_wardrobe, list_storage_gun,
                                LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_ALL_THINGS as All_Th,
                                dict_use_storage_trash as dict_u, LEXICON_scribe_trash as LScrTr, dict_NPS,
                                dict_gun,
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

class MeadowsHuntFSM(StatesGroup):
    state_you_win = State()
  #  st_2 = State()
   # st_3 = State()


@router.callback_query(F.data == 'hunting')
async def hunting(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting --- clb.data = {clb.data}")
    logging.info(f'\nstate.get_state() = {await state.get_state()} ------ state.get_data() = {await state.get_data()}')

    dict_kb={'Ok': 'hunting1'}


    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Поиск займет от 3 до 10 минут.\n В РЕЖИМЕ ТЕСТИРОВАНИЯ 0 МИНУТ\n ", reply_markup=keyboard)
    minutes = 0 ###random.randint(3, 10)
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


@router.callback_query(F.data == 'hunting1')
async def hunting1(clb: CallbackQuery):
    logging.info(f"hunting1 --- clb.data = {clb.data}")

    tg_id=clb.message.chat.id
    time_now = datetime.now()
    current_time_minutes = (await rq.get_user_dict(tg_id))['time']
    current_time = datetime.strptime(current_time_minutes.split('!')[0], '%Y-%m-%d %H:%M:%S.%f')
    minutes = int(current_time_minutes.split('!')[1])


    if time_now - timedelta(minutes=minutes) > current_time:
        clb_data_for_check = 'hunting2'
    else:
        clb_data_for_check = 'hunting1'
    dict_kb={'Проверить': clb_data_for_check, 'Выйти': 'st_0'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    #await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    try:
        await clb.message.edit_caption(caption=f"Поиск добычи", reply_markup=keyboard)
    except:
        await clb.message.edit_caption(caption=f"Пoиcк дoбычи.", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'hunting2')
@router.callback_query(F.data == 'hunting2_back')
async def hunting2(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting2 --- clb.data = {clb.data}")

    if clb.data == 'hunting2':
        flora = ['luvron_polevoy', 'blue_rabbit', 'daron']
        random_flora = random.randint(0,2)
        name_flora = flora[random_flora]
        await state.clear()
        # в зависимости от name_flora из заданных диапазонов выбираются ХП противников
        if name_flora == 'luvron_polevoy':
            xp = random.randint(60, 70)
        elif name_flora == 'blue_rabbit':
            xp = random.randint(20, 25)
        elif name_flora == 'daron':
            xp = random.randint(110, 140)
        logging.info(f'\nname_flora = {name_flora}\nxp = {xp}\nrandom_flora = {random_flora}')
        # заносим в состояние выбранное имя противника, дистация 3=дальняя, 2=средняя, 1=ближняя
        await state.update_data({'name_flora': name_flora, 'distance': 3, 'xp': xp})
    else:
        dict_state = await state.get_data()
        name_flora = dict_state['name_flora']
        xp = dict_state['xp']
    dict_kb={All_Th[name_flora]: f'descriptions!{name_flora}', 'Напасть': 'attack', 'Спрятаться': 'hide', 'Бежать': 'run_away'}
    keyboard = kb.create_in_kb(2, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_flora]))

    await clb.message.edit_caption(caption=f"Кто-то приближается!\n\nЭто {All_Th[name_flora]}!\n\n", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'run_away')
async def hunting3(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting3 --- clb.data = {clb.data}")


    dict_kb={'Напасть': 'attack', 'Бежать': 'run_away_end'}
    keyboard = kb.create_in_kb(2, **dict_kb)
    #await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
#
    await clb.message.edit_caption(caption=f"Что бы сбежать вам придется выбросить рюкзак и все что в нем есть!", reply_markup=keyboard)
    #await clb.answer()


@router.callback_query(F.data == 'run_away_end')
async def hunting4(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting4 --- clb.data = {clb.data}")

    # чтобы сбежать, надо выбрасить рюкзак
    await hf.delete_all_things_from_put_on_backpack(tg_id=tg_id, del_backpack_xp='del_backpack_xp')

    rundom_num = random.randint(1,100)
    logging.info(f'rundom_num = {rundom_num}')
    if 1<= rundom_num <= 90:
        dict_kb={'Ok': 'location_meadows_start'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
        await clb.message.edit_caption(caption=f"Вы сбежали!", reply_markup=keyboard)
    else:
        dict_kb={'Ok': 'attack'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption=f"Сбежать не удалось!", reply_markup=keyboard)
        #await clb.answer()



@router.callback_query(F.data == 'attack')
async def hunting5(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting5 --- clb.data = {clb.data}")


    dict_kb={'Ok': 'attack_begin'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await rq.set_user(tg_id, 'time', 0)
#
    await clb.message.edit_caption(caption=f"В бой!", reply_markup=keyboard)
    #await clb.answer()



@router.callback_query(F.data == 'hide')
async def hunting6(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"hunting6 --- clb.data = {clb.data}")


    rundom_num = random.randint(1,100)
    logging.info(f'rundom_num = {rundom_num}')
    if 1<= rundom_num <= 70:
        dict_kb={'Ok': 'location_meadows_start'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
        await clb.message.edit_caption(caption=f"Вас не заметили!", reply_markup=keyboard)
    else:
        dict_kb={'В бой!\n': 'attack_begin'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
        await clb.message.edit_caption(caption=f"Вас заметили!", reply_markup=keyboard)
        #await clb.answer()





####################

@router.callback_query(F.data.startswith('hunt_end'))
async def hunt_end(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    #logging.info(f'\nCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC----------------clb.data = {clb.data}')

    dict_state = await state.get_data()
    if dict_state:
        logging.info(f'\n\ndict_state = {dict_state}')
        xp_flora = dict_state['xp']
        name_flora = dict_state['name_flora']
        distance: dict = {1: 'Ближняя', 2: 'Средняя', 3: 'Дальняя'}
        distance_index = dict_state['distance']

    dict_user = await rq.get_user_dict(tg_id)
    my_xp = dict_user['xp']

    stroka: str = ''

# если сюда перешли по нажатию кнопки
    if clb.data.startswith('hunt_end'):

        # {str_pocket2: f'hunt_end!pocket2!{name_pocket_2}!{value_pocket2}'}],
        # {name_left_hand: f'hunt_end!left_hand!{name_left_hand}!{value_left_hand}'},
        pocket_hand = clb.data.split('!')[-3]
        clb_name = clb.data.split('!')[-2]
        clb_value = clb.data.split('!')[-1]

        # Если был нажат карман, то проверяем есть ли там лекарство, если есть -- восстанавливаем свое ХП
        if pocket_hand.startswith('pocket'):
            if clb_name == 'pusto':
                stroka = 'Использовать карман нельзя\n'
                await clb.message.edit_caption(caption=stroka)
            else:
                # восстановить ХП, вычесть 1 драг из кармана
                recover_xp = await hf.recover_xp_subtracts_drug(
                    tg_id=tg_id,
                    pocket_cell=pocket_hand,
                    name_drug=clb_name,
                    value_drug=int(clb_value)
                )

                if not recover_xp[1]: # т.е. если в кармане не осталось лекарства
                    glagol = 'закончились' if clb_name in ['bandages', 'fried_veins', 'berries'] else ('закончился' if clb_name=='bandages_s' else ('закончилось' if clb_name=='fried_meat' else 'закончилась'))
                    stroka = f'{All_Th[clb_name]} {glagol}\n'
                if stroka:
                    stroka = f'Вы восстановили ХП до {recover_xp[0]} \n' + stroka
                else:
                    stroka = f'Вы восстановили ХП до {recover_xp[0]} \n'
            logging.info(f'stroka = {stroka}')
        # если была нажата кнопка "Отдалиться"
        elif pocket_hand == 'depart':
            await state.update_data({'distance': (await state.get_data())['distance']+1})
            if stroka:
                stroka = f'Вы отдалились \n' + stroka
            else:
                stroka = f'Вы отдалились \n'

        # если была нажата кнопка "Сблизиться"
        elif pocket_hand == 'closer':
            await state.update_data({'distance': (await state.get_data())['distance']-1})
            if stroka:
                stroka = f'Вы сблизились \n' + stroka
            else:
                stroka = f'Вы сблизились \n'

        # [{name_left_hand: f'hunt_end!left_hand!{name_left_hand}!{value_left_hand}'},
        # если была нажата кнопка с каким-то оружием
        elif pocket_hand.endswith('_hand'):
            # можем атаковать
            distance_ = (await state.get_data())['distance']
            nothink = ''
            in_hand = (await rq.get_user_dict(tg_id))[pocket_hand]

            if clb_name == 'G17' and distance_ in [1, 2] or clb_name == 'spear' and distance_ == 1 or nothink == in_hand and distance_ == 1:
                # -1 к ХП оружия
                demage_nps = int(await hf.demage_nps_subtracts_xp_gun(
                    tg_id=tg_id,
                    name_nps=name_flora,
                    gun=clb_name,
                    distance=distance_index,
                    hand=pocket_hand))
                new_xp_nps = xp_flora - demage_nps

                stroka = f'Вы нанесли урон {All_Th[name_flora]} {demage_nps} ХП \n' + stroka
                await state.update_data({'xp': new_xp_nps})
            else:
                stroka = f'Вы не можете атаковать на этой дистанции\n' + stroka


# если сюда перешли БЕЗ нажатия кнопки, а по времени
    else:
        stroka = f"Вы ничего не сделали\n"


# ПЯТИУГОЛЬНИК  НПС МОЖЕТ АТАКОВАТЬ?

    # flora = ['luvron_polevoy', 'blue_rabbit', 'daron']
    # distance: dict = {1: 'Ближняя', 2: 'Средняя', 3: 'Дальняя'}
    if clb.data=='attack_begin': # т.е. если я перешел сюда по кнопке, то атаки быть не может, атака со стороны НПС только по бездействию
        if distance_index in [2, 3]:  # Атаковать не может, сообщение "сблизиться"
            stroka = f"{All_Th[name_flora]} сближается\n" + stroka
            await state.update_data({'distance': distance_index-1})
        list_demage: list = [] # создается пустой список, потом на него проверка

        # если позволяет НПС аттаковать, то формируем список с тремя видами урона
        if name_flora == 'luvron_polevoy' and distance_index == 1:
            list_demage = [random.randint(15,25), random.randint(5,10), 0]
        elif name_flora == 'blue_rabbit' and distance_index == 1:
            list_demage = [random.randint(3, 5), random.randint(1,3), 0]
        elif name_flora == 'daron' and distance_index == 2:
            list_demage = [random.randint(1,5), random.randint(2,10), random.randint(7,35)]
        elif name_flora == 'daron' and distance_index == 1:
            list_demage = [35, 15, 0]

        if list_demage:
            # return [demage, helmet, 0] # Если второй элемент существует, то эта броня уничтожена
            return_demage = await hf.armor_damage_subtracts_xp_percent(tg_id=tg_id, list_demage=list_demage)
            stroka = f"{All_Th[name_flora]} наносит вам урон {return_demage[0]}\n" + stroka
            ###
            if len(return_demage)==3:
                if return_demage[2]>0:
                    stroka = stroka + f"Ресурс {All_Th[return_demage[1]]} снизился до {return_demage[2]} %\n"
                else:
                    stroka = f"{All_Th[return_demage[1]]} уничтожен!\n"
        # установка нового значения моего ХП
            #await rq.set_user(tg_id, 'xp', (await rq.get_user_dict(tg_id))['xp']-10)
        #logging.info(f"\nstroka = {stroka}")


# ИТОГ проверка не погиб ли аватар
    dict_state = await state.get_data()
    xp_flora = dict_state['xp']
    name_flora = dict_state['name_flora']

    distance: dict = {1: 'Ближняя', 2: 'Средняя', 3: 'Дальняя'}
    distance_index = dict_state['distance']

    dict_user = await rq.get_user_dict(tg_id)
    my_xp = dict_user['xp']

    stroka = stroka + f"У вас {my_xp} ХП, у противника {xp_flora} ХП\nДистанция {distance[distance_index]}"
    my_xp = (await rq.get_user_dict(tg_id))['xp']
    xp_flora = (await state.get_data())['xp']

    if my_xp > 0:
        logging.info(f'\nmy_xp = {my_xp}\nxp_flora = {xp_flora}')
        if xp_flora > 0:
            await hunting7(clb=clb, state=state, stroka=stroka)
        else:
            # Вы победили, удалить и обновить state,
            #dict_hunt = {'raw_meat': 2, 'bones': 1, 'veins': 3}
            await state.clear()
            #await state.update_data(dict_hunt)

            await rq.set_user(tg_id, 'time', 'stop')
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
            keyboard = kb.create_in_kb(1, **{'Ok': 'you_are_win'})
            await clb.message.edit_caption(caption=f"Вы победили", reply_markup=keyboard)
            # установка состояния, чтобы из рюкзака потом перходить в состояние "вы победили"
            await state.set_state(MeadowsHuntFSM.state_you_win)
    else:
        # Теряется надетая экипировка Теряется рюкзак теряется все что в карманах Аватар 100ХП появляется на локации "место посадки"
        await rq.set_user(tg_id, 'xp', 100)
        await rq.set_user(tg_id, 'time', 0)
        await rq.set_user(tg_id, 'location', 'landing_place')
        list_user = ['helmet', 'dress', 'shoes', 'left_hand', 'right_hand']
        for elem in list_user:
            await rq.set_user(tg_id, elem, '')
        list_user_xp = ['xp_helmet', 'xp_dress', 'xp_shoes', 'xp_left_hand', 'xp_right_hand']
        for elem in list_user_xp:
            await rq.set_user(tg_id, elem, 0)

        await hf.delete_all_things_from_put_on_backpack(tg_id, 'pocket', 'del_xp_backpack')
        await state.clear()
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        keyboard = kb.create_in_kb(1, **{'Ok': 'checking_where_avatar_is_located'})
        await clb.message.edit_caption(caption=f"Аватар погиб", reply_markup=keyboard)











@router.callback_query(F.data == 'attack_begin')
async def hunting7(clb: CallbackQuery, state: FSMContext, stroka: str|None=None):
    tg_id=clb.message.chat.id
    logging.info(f"hunting7 --- clb.data = {clb.data}")

    # await state.update_data({'name_flora': name_flora, 'distance': 3, 'xp': xp})
    dict_flora = await state.get_data()
    logging.info(f'dict_flora = {dict_flora}')
    xp_flora = dict_flora['xp']
    name_flora = dict_flora['name_flora']
    distance_index = dict_flora['distance']
    dict_user = await rq.get_user_dict(tg_id)
    my_xp = dict_user['xp']
    # что у игрока в руках
    left_hand = dict_user['left_hand']
    if left_hand:
        name_left_hand = left_hand.split('!')[0]
        value_left_hand = left_hand.split('!')[1]
    else:
        name_left_hand = 'nothink'
        value_left_hand = ''
    right_hand = dict_user['right_hand']
    if right_hand:
        name_right_hand = right_hand.split('!')[0]
        value_right_hand = right_hand.split('!')[1]
    else:
        name_right_hand = 'nothink'
        value_right_hand = ''
    distance: dict = {1: 'Ближняя', 2: 'Средняя', 3: 'Дальняя'}

    # что лежит в карманах
    pocket1 = await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(tg_id, 'pocket1')
    if pocket1[0]:
        str_pocket1 = f'{All_Th[pocket1[0]]} {pocket1[1]} шт.'#await hf.modify_dict_with_all_things_from_backpack_to_srt_with_enter(pocket1)
        name_pocket_1 = pocket1[0]
        value_pocket1 = pocket1[1]
    else:
        str_pocket1, name_pocket_1, value_pocket1 = 'Пусто', 'pusto', 'Y'
    pocket2 = await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(tg_id, 'pocket2')
    if pocket2[0]:
        str_pocket2 = f'{All_Th[pocket2[0]]} {pocket2[1]} шт.'#await hf.modify_dict_with_all_things_from_backpack_to_srt_with_enter(pocket2)
        name_pocket_2 = pocket2[0]
        value_pocket2 = pocket2[1]
    else:
        str_pocket2, name_pocket_2, value_pocket2 = 'Пусто', 'pusto', 'Y'


    list_kb=[
        [{str_pocket1: f'hunt_end!pocket1!{name_pocket_1}!{value_pocket1}'},
         {str_pocket2: f'hunt_end!pocket2!{name_pocket_2}!{value_pocket2}'}],
            [{All_Th[name_left_hand]: f'hunt_end!left_hand!{name_left_hand}!{value_left_hand}'},
             {All_Th[name_right_hand]: f'hunt_end!right_hand!{name_right_hand}!{value_right_hand}'}]]

    if distance_index == 3:
        list_kb.append([{'Сблизиться': f'hunt_end!closer!NO!{distance_index}'}])
    elif distance_index == 2:
        list_kb.append([{'Сблизиться': f'hunt_end!closer!NO!{distance_index}'}])
        list_kb.append([{'Отойти': f'hunt_end!depart!NO!{distance_index}'}])
    elif distance_index == 1:
        list_kb.append([{'Отойти': f'hunt_end!depart!NO!{distance_index}'}])


    keyboard = kb.create_in_kb_from_list_dict(list_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N20']))
    if stroka:
        await clb.message.edit_caption(caption=stroka, reply_markup=keyboard)
    else:
        await clb.message.edit_caption(
            caption=
            f"У вас {my_xp} ХП, у противника {xp_flora} ХП\n"
            f"Дистанция {distance[distance_index]}",
            reply_markup=keyboard)

    #logging.info(f'\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA----------------clb.data = {clb.data}')

    await asyncio.sleep(5)
    if clb.data.startswith('attack') and (await rq.get_user_dict(tg_id))['location']=='location_meadows' and (await rq.get_user_dict(tg_id))['time']!='stop':

        await hunt_end(clb=clb, state=state)

   # logging.info(f'\nBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB----------------clb.data = {clb.data}')



@router.callback_query(F.data == 'you_are_win')
async def you_are_win(clb: CallbackQuery, state: FSMContext):
    tg_id=clb.message.chat.id
    logging.info(f"you_are_win --- clb.data = {clb.data}")

    #await rq.set_user(tg_id, 'time', 0)
    dict_hunt = {'raw_meat': 2, 'bones': 1, 'veins': 3}
    await state.update_data(dict_hunt)

    keyboard = kb.create_list_in_kb(
    width=2,
    dict_=dict_hunt,
    prefix1='descriptions!',
    prefix2='what_do_hunt!',
    backpack_clb_back='backpack', # рюкзак
    take_all_='hunt', # взять всё       take_all_' есть  в колбэке, чтобы не спутать с hunt
    do_not_take_='hunt' # не брать      'do_not_take_' есть  в колбэке, чтобы не спутать с hunt
    )
    await clb.message.edit_caption(caption=f"Вы победили", reply_markup=keyboard)


@router.callback_query(F.data.startswith('what_do_hunt!'))
async def what_do_hunt(clb: CallbackQuery):
    #tg_id=clb.message.chat.id
    logging.info(f"what_do_hunt --- clb.data = {clb.data}")
    name_loot = clb.data.split('!')[-2]
    number_loot = clb.data.split('!')[-1]
    dict_kb={'Положить в рюкзак': f'put_on_backpack_hunt!{name_loot}!{number_loot}',
             'Использовать': f'use_hunt!{name_loot}!{number_loot}',
             'Назад': 'you_are_win',
             }
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N21']))
    await clb.message.edit_caption(caption=f"Что делаем с {All_Th[name_loot.upper()]} {number_loot} шт", reply_markup=keyboard)
    #await clb.answer()