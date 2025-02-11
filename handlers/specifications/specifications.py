from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import and_f, or_f
from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut, LEXICON_ALL_THINGS as All_Th,
                                LEXICON_scribe_trash as LScrTr, LEXICON_scribe_wardrobe as LScrWard,
                                dict_gun_description as dgd, dict_armor, dict_percent_xp)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf
from aiogram.fsm.context import FSMContext
#from handlers.location_anather_h.meadows_loot import MeadowsLootFSM

router = Router()

import logging


# spec1 --- specifications_inner
@router.callback_query(F.data == 'specifications_inner')
@router.callback_query(F.data == 'specifications_lp')
@router.callback_query(F.data == 'specifications_meadows')
@router.callback_query(F.data == 'specifications_go_to')
async def spec1(clb: CallbackQuery, state: FSMContext):
    logging.info(f'spec1')
    tg_id = clb.message.chat.id
    if clb.data != 'specifications_inner': # если пришли с
        if clb.data == 'specifications_lp':
            clb_back = 'start'
        elif clb.data == 'specifications_meadows':
            clb_back = 'location_meadows'
        elif clb.data == 'specifications_go_to':
            clb_back = 'location_go_to_back'
        await rq.set_backpack_leana(tg_id, 'xp', clb_back)
    else:
        clb_back = (await rq.get_BackpackLeana(tg_id))['xp']

    #if await state.get_state() == MeadowsLootFSM.state_meadows1:
    #    clb_back = 'location_meadows'
    #else:
    #    clb_back = 'start'

    dict_kb={'Общие': 'overall_spec', 'Брони': 'armor_spec',
            'Оружия': 'gun_spec', 'Назад': clb_back,}
    keyboard = kb.create_in_kb(2, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N4']))
    await clb.message.edit_caption(caption='Характеристики', reply_markup=keyboard)
    await state.clear()




# spec2 --- overall_spec
@router.callback_query(F.data == 'overall_spec')
async def spec2(clb: CallbackQuery):
    logging.info(f'spec2')

    # запрос в БД
    data_user = await rq.get_user_dict(tg_id=clb.message.chat.id)
    name_user = data_user['name_user']
    if name_user == 'username':
        name_user = clb.message.chat.id
    xp = data_user['xp']
    kristals = data_user['kristals']
    bio = (await rq.get_StorageBIO(tg_id=clb.message.chat.id))['bio']

    dict_kb={'Назад': 'specifications_inner',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N4']))
    await clb.message.edit_caption(
        caption=f'Имя {name_user}\n❤️(хп) {xp}\n🛢️(биоресурс) {bio}\n💎(кристаллы) {kristals}\n\n',
        reply_markup=keyboard)
    await clb.answer()



# spec3 --- gun_spec
@router.callback_query(F.data == 'gun_spec')
async def spec3(clb: CallbackQuery):
    logging.info(f'spec3')
    tg_id=clb.message.chat.id

    # запрос в БД
    data_user = await rq.get_user_dict(tg_id)
    left_hand = data_user['left_hand'] #.split('!') if '!' in left_hand else data_user['left_hand']
    right_hand = data_user['right_hand']# .split('!') if '!' in right_hand else data_user['right_hand']

    # по умолчанию ставим текст и колбэки на '' на ничего
    # и в условии, что оружие есть - меняем
    text_left_hand, text_right_hand = "[⚔1 Отсутствует]", "[⚔2 Отсутствует]"
    clb_left, clb_right =  'no!gun_in_hand', 'no!gun_in_hand'
    text_left_percent, text_right_percent = f"[{dgd['nothink'][0]}]", f"[{dgd['nothink'][0]}]"
    clb_left_percent, clb_right_percent = 'left_hand!gun_percent', 'right_hand!gun_percent'

    list_dict: list =[]

    if 'G17' in left_hand or 'spear' in left_hand:
    # например так, с восклицательным знаком G17!10
        list_ = left_hand.split('!')
        xp = data_user['xp_left_hand']
        new_percent = (100 * xp) / dict_percent_xp[list_[0]]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)

        if new_percent >=1: # зануляем в талице User
            await rq.set_user(tg_id, 'left_hand', f'{list_[0]}!{new_percent}')
            text_left_hand = f"[⚔1 {All_Th[list_[0]]}]"
            clb_left = f'{list_[0]}!gun_in_hand'

            text_left_percent = f'[{new_percent}% {dgd[list_[0]][0]}]' # правая часть, процентовка
        #clb_left_percent = f'{list_[0]}!gun_percent'
    list_dict.append([{text_left_hand: clb_left}, {text_left_percent: clb_left_percent}])


    if 'G17' in right_hand or 'spear' in right_hand:
    # например так, с восклицательным знаком G17!10
        list_ = right_hand.split('!')
        xp = data_user['xp_right_hand']
        new_percent = (100 * xp) / dict_percent_xp[list_[0]]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)


        if new_percent >=1: # зануляем в талице User
            await rq.set_user(tg_id, 'right_hand', f'{list_[0]}!{new_percent}')
            text_right_hand = f"[⚔2 {All_Th[list_[0]]}]"
            clb_right = f'{list_[0]}!gun_in_hand'

            text_right_percent = f'[{new_percent}% {dgd[list_[0]][0]}]'
        #clb_right_percent = f'{list_[0]}!gun_percent'
    list_dict.append([{text_right_hand: clb_right}, {text_right_percent: clb_right_percent}])

    list_dict.append([{'Назад': 'specifications_inner'}])
    #logging.info(f'list_dict = {list_dict}')
    keyboard = kb.create_in_kb_from_list_dict(list_dict=list_dict)
    await clb.message.edit_caption(
        caption='Оружие в руках:\n',
        reply_markup=keyboard,
        parse_mode=None
    )



# spec4 --- F.data.endwith('gun_spec')
@router.callback_query(F.data.endswith('gun_in_hand'))
async def spec4(clb: CallbackQuery):
    logging.info(f'spec4 --- clb.data = {clb.data}')

    name_gun = clb.data.split('!')[0]
    str_answer:str ='PUSTO'
    if name_gun == 'no':
        str_answer = 'Оружие отсутствует'
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17'])) # красный крест
    elif name_gun == 'G17':
        str_answer = dgd['G17_description']
        logging.info(f'name_gun = {name_gun} --- str_answer = {str_answer}')
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N22']))
    elif name_gun == 'spear':
        str_answer = dgd['spear_description']
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N23']))
    await clb.message.edit_caption(
        caption=str_answer,
        reply_markup=kb.create_in_kb(1, **{'Назад': 'gun_spec'}),
        parse_mode=None)
    await clb.answer()



# spec5 --- F.data == 'armor_spec'
@router.callback_query(F.data == 'armor_spec')
async def spec5(clb: CallbackQuery):
    logging.info(f'spec5 --- clb.data = {clb.data}')

    tg_id=clb.message.chat.id
    # запрос в БД. Что надето? (рюкзак, шлем, костюм, ботинки)
    data_user = await rq.get_user_dict(tg_id)
    backpack = data_user['backpack'] ###.split('!') if '!' in left_hand else data_user['left_hand']
    helmet = data_user['helmet']  ### .split('!') if '!' in right_hand else data_user['right_hand']
    dress = data_user['dress']
    shoes = data_user['shoes']

    list_dict: list = []
    text_helmet, text_dress, text_shoes, text_backpack = '', '', '', '' # текст на кнопке, пока пусто, дальше модифицируем
    clb_helmet, clb_dress, clb_shoes, clb_backpack = 'helmet!no_armor', 'dress!no_armor', 'shoes!no_armor', 'backpack!no_armor' # колбэк, если пусто

    if 'helmet' in helmet:
        # например так, с восклицательным знаком helmet_kosmonavt!5
        name_armor = helmet.split('!')[0] # helmet_kosmonavt
        text_helmet = f"🪖-{All_Th[name_armor]}" # шлем космонавта
        clb_helmet = f'{name_armor}!armor_description' # helmet_kosmonavt!armor_description

        xp = data_user['xp_helmet'] # перевод актуального ХП в проценты, запись в базу данных актуального процента брони или рюкзака
        new_percent = (100 * xp) / dict_percent_xp[name_armor]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)

        if new_percent >=1: # зануляем в талице User
            text_helmet_percent = f'{new_percent} %' # текст кнопки
            clb_helmet_percent = f'{name_armor}!armor_percent' # колбэк кнопки
            list_dict.append([{text_helmet: clb_helmet}, {text_helmet_percent: clb_helmet_percent}]) # добавляем текст и колбэк кнопок

            # установка нового актуально процента в таблицу User
            await rq.set_user(tg_id, 'helmet', f'{name_armor}!{new_percent}')


        else: # зануляем в талице User эти строки и пишем ОТСУТСТВУЕТ
            await rq.set_user(tg_id, 'helmet', '')
            await rq.set_user(tg_id, 'xp_helmet', '')
            text_helmet = "🪖 Отсутствует"
            list_dict.append([{text_helmet: clb_helmet}])
    else:
        text_helmet = "🪖 Отсутствует"  # clb_helmet = 'helmet!no_armor' установлен по умолчанию
        list_dict.append([{text_helmet: clb_helmet}])




    if 'dress' in dress:
        # например так, с восклицательным знаком backpack_leana!10
        name_armor = dress.split('!')[0]
        text_ = f"🦺-{All_Th[name_armor]}"
        clb_ = f'{name_armor}!armor_description'
        xp = data_user['xp_dress'] # перевод актуального ХП в проценты, запись в базу данных актуального процента брони или рюкзака
        new_percent = (100 * xp) / dict_percent_xp[name_armor]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)
        if new_percent >=1: # зануляем в талице User
            text_percent = f'{new_percent} %' # текст кнопки
            clb_percent = f'{name_armor}!armor_percent' # колбэк кнопки
            list_dict.append([{text_: clb_}, {text_percent: clb_percent}]) # добавляем текст и колбэк кнопок
            # установка нового актуально процента в таблицу User
            await rq.set_user(tg_id, 'dress', f'{name_armor}!{new_percent}')

        else: # зануляем в талице User эти строки и пишем ОТСУТСТВУЕТ
            await rq.set_user(tg_id, 'dress', '')
            await rq.set_user(tg_id, 'xp_dress', '')
            text_ = "🦺 Отсутствует"
            list_dict.append([{text_: clb_}])
    else:
        text_ = "🦺 Отсутствует"
        list_dict.append([{text_: clb_dress}])

    if 'shoes' in shoes:
        # например так, с восклицательным знаком backpack_leana!10
        name_armor = shoes.split('!')[0]
        text_ = f"👞-{All_Th[name_armor]}"
        clb_ = f'{name_armor}!armor_description'
        xp = data_user['xp_shoes'] # перевод актуального ХП в проценты, запись в базу данных актуального процента брони или рюкзака
        new_percent = (100 * xp) / dict_percent_xp[name_armor]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)
        if new_percent >=1: # зануляем в талице User
            text_percent = f'{new_percent} %' # текст кнопки
            clb_percent = f'{name_armor}!armor_percent' # колбэк кнопки
            list_dict.append([{text_: clb_}, {text_percent: clb_percent}]) # добавляем текст и колбэк кнопок
            # установка нового актуально процента в таблицу User
            await rq.set_user(tg_id, 'shoes', f'{name_armor}!{new_percent}')

        else: # зануляем в талице User эти строки и пишем ОТСУТСТВУЕТ
            await rq.set_user(tg_id, 'shoes', '')
            await rq.set_user(tg_id, 'xp_shoes', '')
            text_ = "👞 Отсутствует"
            list_dict.append([{text_: clb_}])
    else:
        text_ = "👞 Отсутствует"
        list_dict.append([{text_: clb_shoes}])


    if 'foliage' in backpack or 'leana' in backpack:
        # например так, с восклицательным знаком backpack_leana!10
        name_armor = backpack.split('!')[0]
        text_ = f"🎒-{All_Th[name_armor]}"
        clb_ = f'{name_armor}!armor_description'
        xp = data_user['xp_backpack'] # перевод актуального ХП в проценты, запись в базу данных актуального процента брони или рюкзака
        new_percent = (100 * xp) / dict_percent_xp[name_armor]
        new_percent = round(new_percent) if new_percent >= 1 else int(new_percent)
        if new_percent >=1: # зануляем в талице User
            text_percent = f'{new_percent} %' # текст кнопки
            clb_percent = f'{name_armor}!armor_percent' # колбэк кнопки
            list_dict.append([{text_: clb_}, {text_percent: clb_percent}]) # добавляем текст и колбэк кнопок
            # установка нового актуально процента в таблицу User
            await rq.set_user(tg_id, 'backpack', f'{name_armor}!{new_percent}')

        else: # зануляем в талице User эти строки и пишем ОТСУТСТВУЕТ
            await rq.set_user(tg_id, 'backpack', '')
            await rq.set_user(tg_id, 'xp_backpack', '')
            text_ = "🎒 Отсутствует"
            list_dict.append([{text_: clb_}])
    else:
        text_ = "🎒 Отсутствует"
        list_dict.append([{text_: clb_backpack}])

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N4']))
    list_dict.append([{'Назад': 'specifications_inner'}])
    #logging.info(f'list_dict = {list_dict}')
    keyboard = kb.create_in_kb_from_list_dict(list_dict=list_dict)
    await clb.message.edit_caption(caption='На вас надето:', reply_markup=keyboard)



# spec6 --- F.data.endwith('!no_armor') F.data.endswith('!armor_description')
@router.callback_query(F.data.endswith('!no_armor'))
@router.callback_query(F.data.endswith('!armor_description'))
async def spec6(clb: CallbackQuery):
    logging.info(f'spec6 --- clb.data = {clb.data}')

    armor = clb.data.split('!')[0]

    if clb.data.endswith('!armor_description'):
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[armor]))


        if armor.startswith('backpack'):
            await clb.message.edit_caption(
                caption=f'{dict_armor[armor][0]} {dict_armor[armor][1]}',
                reply_markup=kb.create_in_kb(1, **{'Назад': 'armor_spec'})
            )
        else:
            await clb.message.edit_caption(
                caption=f'{dict_armor[armor][0]}\nБаллистическая защита-{dict_armor[armor][1]}'
                        f'\nХимическая защита-{dict_armor[armor][2]}\nЭлектрическая защита-{dict_armor[armor][3]}',
                reply_markup=kb.create_in_kb(1, **{'Назад': 'armor_spec'})
            )

    elif clb.data.endswith('no_armor'):
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[armor]))
        if 'backpack' in clb.data:
            answer = 'Рюкзак отсутствует'
        elif 'helmet' in clb.data:
            answer = 'Шлем отсутствует'
        elif 'dress' in clb.data:
            answer = 'Костюм отсутствует'
        else:
            answer = 'Ботинки отсутствуют'
        await clb.message.edit_caption(
                caption=answer,
                reply_markup=kb.create_in_kb(1, **{'Назад': 'armor_spec'})
            )



# spec7 --- F.data.endwith('!armor_percent') --- F.data.endswith('armor_percent_backpack')
@router.callback_query(F.data.endswith('armor_percent'))
@router.callback_query(F.data.endswith('armor_percent_backpack'))
@router.callback_query(F.data.endswith('gun_percent')) # spear!gun_percent
async def spec7(clb: CallbackQuery):
    logging.info(f"spec7 --- armor = clb.data.split('!')[0] = {clb.data.split('!')[0]} --- clb.data = {clb.data}")

    # Здесь также обрабатывается и Gun. Но переменная будет у всех armor
    # Для оружия armor это left_hand right_hand

    armor = clb.data.split('!')[0]

    data_user = await rq.get_user_dict(tg_id=clb.message.chat.id)
    if 'helmet' in armor or 'dress' in armor or 'shoes' in armor or 'backpack' in armor: # например helmet_kosmonavt!55
        part_armor = armor.split('_')[0] # например helmet
        percent = data_user[part_armor].split('!')[-1]
        logging.info(f'armor{armor} --- percent = {percent}')
    elif ('left_hand'==armor and data_user[armor] == '') or ('right_hand'==armor and data_user[armor] == ''):
        armor = 'nothink'
        logging.info(f' nothink --- armor = {armor}')
    else: # например G17!55
        percent = data_user[armor].split('!')[-1] # например G17
        armor = data_user[armor].split('!')[0] # переопределяем armor для оружия. Вместо left_hand right_hand
        logging.info(f'armor = {armor} --- percent = {percent}')

    location = data_user['location']

    await clb.message.edit_media(media=InputMediaPhoto(media=ph[armor])) # это одна на всех смена картинки по названию вещи = armor


    if armor.startswith('backpack'): # для рюкзаков РЮКЗАК можно снять в ЛЮБОЙ локации
            keyboard = kb.create_in_kb(1, **{'Снять': f'{clb.data}!put_off_backpack', 'Назад': 'armor_spec'})

    # у рюкзака clb.data = list_[0]}!armor_percent_backpack', у остальных list_[0]}!armor_percent'
    if location == 'landing_place': # снять бронню и оружие можно только на Локации 'landing_place'
        if 'helmet' in armor or 'dress' in armor or 'shoes' in armor: # для брони
            keyboard = kb.create_in_kb(1, **{'Снять': f'{clb.data}!put_off_armor', 'Назад': 'armor_spec'})
        elif 'G17' in armor or 'spear' in armor or 'nothink' in armor: # для  оружия
            if armor == 'nothink': # модифицируем клавиатуру. Для остальных кнопка снять присутствует
                keyboard = kb.create_in_kb(1, **{'Назад': 'gun_spec'})
            else:
                keyboard = kb.create_in_kb(1, **{'Снять': f'{clb.data}!put_off_armor', 'Назад': 'gun_spec'})

    else: # НЕ для локации 'landing_place'
        if clb.data.endswith('armor_percent'):
            keyboard = kb.create_in_kb(1, **{'Назад': 'armor_spec'})
        else:
            keyboard = kb.create_in_kb(1, **{'Назад': 'gun_spec'})

    if armor.startswith('backpack'): # для рюкзака
        await clb.message.edit_caption(
            caption=f'{percent}% состояние рюкзака\n {dict_armor[armor][1]}', #dict_armor[armor][1] = '4 ячейки рюкзака \n 2 кармана'
            reply_markup=keyboard
        )

    elif armor in ['G17', 'spear', 'nothink']: # для оружия

        await clb.message.edit_caption(
            caption=
                f'Дальний бой {dgd[f"{armor}_battle"][0][0]}\n'
                f'Средний бой {dgd[f"{armor}_battle"][0][1]}\n'
                f'Ближний бой {dgd[f"{armor}_battle"][0][2]}\n',
            reply_markup=keyboard
        )


    elif part_armor in ['helmet', 'dress', 'shoes']: # для брони
        b_demage, h_demage, e_demage =  dict_armor[armor][1], dict_armor[armor][2], dict_armor[armor][3]


        ### жду пояснений как рассчитываь новые проценты
        ### Здесь будет функция, которая можифицирует b_demage, h_demage, e_demage

        await clb.message.edit_caption(
            caption=f'{percent}%-состояние брони\n{b_demage}%-защита от баллистического урона\n'
                    f'{h_demage}%-защита от химического урона\n{e_demage}%-защита от химического урона',
            reply_markup=keyboard
        )



# spec8 --- F.data.endwith('!put_off_armor')
@router.callback_query(F.data.endswith('!put_off_armor'))#, and_f (F.data.startswith('helmet'), F.data.startswith('dress'), F.data.startswith('shoes'))) #
async def spec8(clb: CallbackQuery):
    logging.info(f'spec8 --- clb.data = {clb.data}')

    # right_hand!gun_percent!put_off_armor
    if 'helmet' in clb.data or 'dress' in clb.data or 'shoes' in clb.data:
        armor = clb.data.split('!')[0]
        data_armor = (await rq.get_user_dict(tg_id=clb.message.chat.id))[armor.split('_')[0]]
        percent = data_armor.split('!')[-1]
    else:
        hand = clb.data.split('!')[0]
        data_armor = (await rq.get_user_dict(tg_id=clb.message.chat.id))[hand]
        armor = data_armor.split('!')[0]
        percent = data_armor.split('!')[1]


    # Если рюкзак не надет, то кнопка "рюкзак" не нужна
    backpack = await hf.what_backpack_put_on(tg_id=clb.message.chat.id)
    if backpack in ['backpack_foliage', 'backpack_leana']:
        if 'helmet' in clb.data or 'dress' in clb.data or 'shoes' in clb.data:
            keyboard = kb.create_in_kb(2, **{'шкаф':f'{armor}!{percent}!put_off_armor_wardrobe', 'рюкзак': f'{armor}!{percent}!put_off_armor_backpack', 'Назад': 'armor_spec'})
        else:
            keyboard = kb.create_in_kb(2, **{'шкаф':f'{armor}!{percent}!{hand}!put_off_armor_wardrobe', 'рюкзак': f'{armor}!{percent}!{hand}!put_off_armor_backpack', 'Назад': 'gun_spec'})
    else:
        if 'helmet' in clb.data or 'dress' in clb.data or 'shoes' in clb.data:
            keyboard = kb.create_in_kb(2, **{'шкаф':f'{armor}!{percent}!put_off_armor_wardrobe', 'Назад': 'armor_spec'})
        else:
            keyboard = kb.create_in_kb(2, **{'шкаф':f'{armor}!{percent}!{hand}!put_off_armor_wardrobe', 'Назад': 'gun_spec'})
    await clb.message.edit_caption(
            caption=f'Куда снимаем\n{All_Th[armor]} {percent}%\n\n',
            reply_markup=keyboard
        )


# spec9 --- F.data.endswith('backpack_armor_percent') --- F.data.endswith('!put_off_armor_wardrobe')
@router.callback_query(F.data.endswith('put_off_backpack')) #  у рюкзака clb.data = list_[0]}!backpack_armor_percent'
@router.callback_query(F.data.endswith('!put_off_armor_wardrobe'))
async def spec9(clb: CallbackQuery):
    logging.info(f'spec9 --- clb.data = {clb.data}')

    tg_id=clb.message.chat.id

    if clb.data.endswith('!put_off_armor_wardrobe'): # если положить в шкаф
        armor = clb.data.split('!')[0]
        percent = clb.data.split('!')[1]
    else: # если положить в рюкзак
        armor = clb.data.split('!')[0]
        data_backpack = (await rq.get_user_dict(tg_id))[armor.split('_')[0]]
        percent = data_backpack.split('!')[-1]
        xp_armor = (await rq.get_user_dict(tg_id))[armor.split('_')[0]]

    #if 'G17' in clb.data or 'spear' in clb.data or 'nothink' in clb.data:
     #   hand = clb.data.split('!')[2]

    if 'backpack' in clb.data: # из надетого рюкзака перед снятием удаляем все вещи
        await hf.delete_all_things_from_put_on_backpack(tg_id)### надо ли удолять из User рюкзак и хп?

    ### Из таблицы User убрать  в Шкаф положить
    if 'helmet' in clb.data or 'dress' in clb.data or 'shoes' in clb.data or 'backpack' in clb.data:
        new_percent = await hf.put_off_armor_or_gun_and_take_this_on_wardrobe_or_backpack(
            tg_id=tg_id,
            armor_or_gun=armor,
            wardrobe_or_backpack='wardrobe'
        )
        #if 'backpack' not in clb.data:
        #    await rq.set_user(tg_id=tg_id, name_column=armor.split('_')[0], current_value='')
        #else:
        #    await rq.set_user(tg_id=tg_id, name_column=armor.split('_')[0], current_value='no_backpack')
    else: # для оружия
        hand = clb.data.split('!')[2]
        new_percent = await hf.put_off_armor_or_gun_and_take_this_on_wardrobe_or_backpack(
            tg_id=clb.message.chat.id,
            armor_or_gun=armor,
            wardrobe_or_backpack='wardrobe',
            hand = hand
        )
        await rq.set_user(tg_id=tg_id, name_column=hand, current_value='')
        logging.info(f'hand = {hand}')

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N24']))
    await clb.message.edit_caption(
            caption=f'Вы положили в шкаф\n{All_Th[armor]} {new_percent}%\n\n',
            reply_markup=kb.create_in_kb(1, **{'ок':'checking_where_avatar_is_located'})
        )


# spec10 --- F.data.endswith('put_off_armor_backpack')
@router.callback_query(F.data.endswith('put_off_armor_backpack'))
async def spec10(clb: CallbackQuery):
    logging.info(f'spec10 --- clb.data = {clb.data}')
    armor = clb.data.split('!')[0]
    percent = clb.data.split('!')[1]

    if 'G17' in clb.data or 'spear' in clb.data or 'nothink' in clb.data:
        hand = clb.data.split('!')[2]
    else:
        hand = 'nohand'



    tg_id = clb.message.chat.id
    #backpack = await hf.what_backpack_put_on(tg_id=tg_id)
    list_cell_button: list = await hf.create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(
        tg_id=tg_id,
        prefix=f'spec10?{armor}?{percent}?{hand}'
    )
    logging.info(f'list_cell_button --- list_cell_button --- list_cell_button = {list_cell_button}')
    if 'G17' in clb.data or 'spear' in clb.data or 'nothink' in clb.data:
        keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell_button, clb_back=f'{hand}!{percent}!put_off_armor')
    else:
        keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell_button, clb_back=f'{armor}!{percent}!put_off_armor')
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
    await clb.message.edit_caption(
            caption=f'В какую ячейку кладём?\n{All_Th[armor]} {percent}%\n\n',
            reply_markup=keyboard)


# spec11 --- F.data.startswith('spec10')
@router.callback_query(F.data.startswith('spec10'))
async def spec11(clb: CallbackQuery):
    logging.info(f'spec11 --- clb.data = {clb.data}') # prefix=f'spec10?{armor}?{percent}' clb.data = spec10!green!backpack_leana!cell_2

    tg_id = clb.message.chat.id
    armor = clb.data.split('?')[1]
    percent = clb.data.split('?')[2]
    hand = clb.data.split('?')[3].split('!')[0]

    #backpack = clb.data.split('!')[-2]
    color = clb.data.split('!')[-3]
    cell = clb.data.split('!')[-1]

    if color == 'red':
        keyboard = kb.create_in_kb(1, **{'Назад': f'{armor}!{percent}!{hand}!put_off_armor_backpack'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(
            caption=f'Сюда положить нельзя\n',
            reply_markup=keyboard)

    elif color == 'green':
        keyboard = kb.create_in_kb(1, **{'Ок': 'checking_where_avatar_is_located'})



        if 'helmet' in armor or 'dress' in armor or 'shoes' in armor or 'backpack' in armor:

            if 'backpack' not in armor:
                await rq.set_user(tg_id=tg_id, name_column=armor.split('_')[0], current_value='')
            else:
                await rq.set_user(tg_id=tg_id, name_column=armor.split('_')[0], current_value='no_backpack')
        else:
            await rq.set_user(tg_id=tg_id, name_column=hand, current_value='')




        await rq.set_user(tg_id, armor.split('_')[0], '')
        await rq.set_backpack_and_cell_with_chek_put_on_backpack(
            tg_id=tg_id,
            #name_column_backpack=cell,
            #current_value_backpack=percent,
            cell=cell,
            name_column_cell=armor,
            current_value_cell=percent
        )

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N6']))
        await clb.message.edit_caption(
            caption=f'Вы положили\n {All_Th[armor]} {percent} % в {LBut[cell.upper()]}',
            reply_markup=keyboard)
