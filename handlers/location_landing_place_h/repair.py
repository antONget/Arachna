from aiogram import F, Router, Bot

from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                list_storage_wardrobe as lsw, list_storage_gun as lsg,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_storage_trash_bio,
                                LEXICON_ALL_THINGS as All_Th, dict_repair_description, dict_repair, )
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf

router = Router()

storage = MemoryStorage()

import logging


# rep1 -- repair
@router.callback_query(F.data == 'repair')
async def repair(clb: CallbackQuery,  state: FSMContext):
    logging.info(f'repair --callback_data = {clb.data}')
    logging.info(f'\nstate.get_state() = {await state.get_state()} ------ state.get_data() = {await state.get_data()}')

    dict_kb={LL['armor']: 'rep1!armor', LL['guns']: 'rep1!guns',
            LBut['back']: 'laboratory',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption=LL['rep1'], reply_markup=keyboard)
    await clb.answer()



# rep1 -- rep1_
@router.callback_query(F.data.startswith('rep1'))
async def rep1(clb: CallbackQuery,  bot: Bot):
    logging.info(f'rep1 --callback_data = {clb.data}')

    clb_button = clb.data.split('!')[1]
    tg_id = clb.message.chat.id

    if clb_button == "armor":
        data_=await rq.get_StorageWardrobe(tg_id=tg_id)
        dict_ = await hf.modify_dict_to_dict_with_count_value(data_)

        # проверям условие, что в хранилище что-то есть
        if not dict_:# если словарь пустой
            dict_kb = {LBut['back']: 'repair'}
            keyboard = kb.create_in_kb(1, **dict_kb)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N24']))
            await clb.message.edit_caption(caption='Брони нет, ремонтировать нечего', reply_markup=keyboard)
            await clb.answer()

        else: # если словарь НЕ пустой

            keyboard = kb.create_list_in_one_row_kb_repair(
                dict_= dict_, prefix='rep2', clb_back_str='repair')

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N24']))
            await clb.message.edit_caption(caption='Что ремонтировать?', reply_markup=keyboard)


    elif clb_button == 'guns':
        data_=await rq.get_StorageGun(tg_id=tg_id)
        dict_ = await hf.modify_dict_to_dict_with_count_value(data_)

        if not dict_:# если словарь пустой
            dict_kb = {LBut['back']: 'repair'}
            keyboard = kb.create_in_kb(1, **dict_kb)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N39']))
            await clb.message.edit_caption(caption='Оружия нет, ремонтировать нечего', reply_markup=keyboard)
            await clb.answer()

        else: # если словарь НЕ пустой

            keyboard = kb.create_list_in_one_row_kb_repair(
                dict_= dict_, prefix='rep2', clb_back_str='repair')

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N39']))
            await clb.message.edit_caption(caption='Что ремонтировать?', reply_markup=keyboard)



@router.callback_query(F.data.startswith('rep2'))
async def rep2(clb: CallbackQuery):
    logging.info(f'rep2 -- callback_data = {clb.data}')
    tg_id = clb.message.chat.id

    clb_name = clb.data.split('!')[1]
    if clb_name in ['spear', 'G17']:
        data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
        answer = 'В oружейной находится'
    else:
        data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
        answer = 'В Xранилище шкаф находится'

    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things.update({f"[{All_Th[clb_name]} {value} шт. {key}%]": f"rep3!{clb_name}!{value}!{key}"})
# модифицируем этот словарь в список списков
    list_button: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    #logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button,
        back=0,
        forward=2,
        count=5,
        clb_name=clb_name,
        clb_button_back='repair',
        prefix_wardrobe='rep'
    )

    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=answer, reply_markup=keyboard)
    await clb.answer()


# >>>>
@router.callback_query(F.data.startswith('rep_forward'))
async def process_forward(clb: CallbackQuery) -> None:
    logging.info(f'process_forward: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    forward = int(clb.data.split('!')[-2]) + 1
    back = forward - 2


    if clb_name in ['spear', 'G17']:
        data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"

    else:
        data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"


    #data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things.update({f"[{All_Th[clb_name]} {value} шт. {key}%]": f"rep3!{clb_name}!{value}!{key}"})
# модифицируем этот словарь в список списков
    list_button_wardrobe: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button_wardrobe,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='repair',
        prefix_wardrobe='rep'
    )

    #keyboard = kb.kb_choise_learners(action='delete_learner', list_learners=list_learners, back=back, forward=forward, count=6)
    if clb_name in ['spear', 'G17']:
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        try:
            await clb.message.edit_caption(caption='В оружeйнoЙ находится', reply_markup=keyboard)
        except:
            await clb.message.edit_caption(caption='B opужейной наxодится', reply_markup=keyboard)
        await clb.answer()

    else:
        data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        try:
            await clb.message.edit_caption(caption='В Хранилище шкаф находится', reply_markup=keyboard)
        except:
            await clb.message.edit_caption(caption='В Хранилищe шкаф находится', reply_markup=keyboard)
        await clb.answer()


# <<<<
@router.callback_query(F.data.startswith('rep_back'))
async def process_forward(clb: CallbackQuery) -> None:
    logging.info(f'process_back: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    back = int(clb.data.split('!')[-2]) - 1
    forward = back + 2

    if clb_name in ['spear', 'G17']:
        data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"

    else:
        data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"

    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things.update({f"[{All_Th[clb_name]} {value} шт. {key}%]": f"rep3!{clb_name}!{value}!{key}"})
# модифицируем этот словарь в список списков
    list_button: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    #logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='repair',
        prefix_wardrobe='rep'
    )
    if clb_name in ['spear', 'G17']:
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        try:
            await clb.message.edit_caption(caption='В оружeйнoЙ находится', reply_markup=keyboard)
        except:
            await clb.message.edit_caption(caption='B opужейной наxодится', reply_markup=keyboard)
        await clb.answer()

    else:
        data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        try:
            await clb.message.edit_caption(caption='В Хранилище шкаф находится', reply_markup=keyboard)
        except:
            await clb.message.edit_caption(caption='В Хранилищe шкаф находится', reply_markup=keyboard)
        await clb.answer()


@router.callback_query(F.data.startswith('rep3'))
async def rep3(clb: CallbackQuery):
    logging.info(f'rep3 -- callback_data = {clb.data}') # rep3!dress_reinforced!1!23'
    tg_id = clb.message.chat.id

    clb_name = clb.data.split('!')[-3]
    value = clb.data.split('!')[-2]
    percent = int(clb.data.split('!')[-1])

    bio = (await rq.get_StorageBIO(tg_id))['bio']
    logging.info(f'ВНИМАНИЕ bio = {bio}')
    kristals = (await rq.get_user_dict(tg_id))['kristals']
    xp = await hf.change_xp_percent_and_back(clb_name, percent)
    flag: bool = False
    trash = await rq.get_StorageTrash(tg_id)
    # формирование текста в зависимости от вещи и её процента
    if percent > 50: # ремонтируется только с использованием БИО
                      # NOT                     NOT
        if 'kosmonavt' not in clb_name and 'G17' not in clb_name: # проверка, что вещи обычные (не платные) (у платных два варианта ремонта, с кристалами)
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][0][0]} ХП\n{dict_repair[clb_name][0][1]} био'
            if bio >= dict_repair[clb_name][0][1]:
                flag = True
        elif 'kosmonavt' in clb_name or 'G17' in clb_name: ### логика этих проверок будет прописываться в следующем хендлере, т.к. можно 2-мя способами отремонтироваться
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][0][0]} ХП\n{dict_repair[clb_name][0][1]} био\nили\n+{dict_repair[clb_name][1][0]} ХП\n{dict_repair[clb_name][1][1]} био\n{dict_repair[clb_name][1][2]} кристалов'
            #flag = 'no_flag'    если больше 50 есть выбор или 1 или 2 словарь НАДО ДЕЛАТЬ ПРОВЕРКУ
            # если меньше 50 выбора нет, только последний словарь

    else: # eсли ХП <= 50%  используется второй словарь
        if 'wanderer' in clb_name or clb_name == 'backpack_foliage':#'kosmonavt' not in clb_name and 'G17' not in clb_name and 'spear' not in clb_name and : # проверка, что вещи обычные (не платные) (у них два варианта ремонта, с кристалами)
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][1][0]} ХП\nСтебель желтоцвета {dict_repair[clb_name][1][1]} шт.\nПалка {dict_repair[clb_name][1][2]} шт.\nЛистья лозы {dict_repair[clb_name][1][3]} шт.\n{dict_repair[clb_name][1][4]} био'
            if trash['yel_fl'] >= dict_repair[clb_name][1][1] and trash['stick'] >= dict_repair[clb_name][1][2] and trash['vine_leaves'] >= dict_repair[clb_name][1][3] and bio >= dict_repair[clb_name][1][4]:
                flag = True
        elif 'reinforced' in clb_name or clb_name == 'backpack_leana':
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][1][0]} ХП\nКости {dict_repair[clb_name][1][1]} шт.\nЖилы {dict_repair[clb_name][1][2]} шт.\n{dict_repair[clb_name][1][3]} био'
            if trash['bones'] >= dict_repair[clb_name][1][1] and trash['veins'] >= dict_repair[clb_name][1][2] and bio >= dict_repair[clb_name][1][3]:
                flag = True
        elif clb_name == 'spear':
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][1][0]} ХП\nПалка {dict_repair[clb_name][1][1]} шт.\nКости {dict_repair[clb_name][1][2]} шт.\nЖилы {dict_repair[clb_name][1][3]} шт.\n{dict_repair[clb_name][1][4]} био'
            if trash['stick'] >= dict_repair[clb_name][1][1] and trash['bones'] >= dict_repair[clb_name][1][2] and trash['veins'] >= dict_repair[clb_name][1][3] and bio >= dict_repair[clb_name][1][4]:
                flag = True
        elif 'kosmonavt' in clb_name: # только второй словарь
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][1][0]} ХП\n{dict_repair[clb_name][1][1]} био\n{dict_repair[clb_name][1][2]} кристалов'
            if bio >= dict_repair[clb_name][1][1] and kristals >= dict_repair[clb_name][1][2]:
                flag = True
        elif clb_name == 'G17':  # у G17 три внутренних словаря --- только третий словарь
            str_answer = f'{All_Th[clb_name]} {percent}% ({xp} ХП)\nПочинить +{dict_repair[clb_name][2][0]} ХП\n{dict_repair[clb_name][2][1]} био\n{dict_repair[clb_name][2][2]} кристалов'
            if bio >= dict_repair[clb_name][2][1] and kristals >= dict_repair[clb_name][2][2]:
                flag = True

    if clb_name in ['helmet_kosmonavt', 'dress_kosmonavt', 'shoes_kosmonavt', 'G17'] and percent > 50:
        dict_kb={'Починить c кристаллами': f'rep4_kristals!{flag}!{clb_name}!{value}!{percent}',
                 'Починить без кристаллов': f'rep4_without_kristals!{flag}!{clb_name}!{value}!{percent}', 'Назад': f'rep2!{clb_name}',}
    else:
        dict_kb={'Починить': f'rep4!{flag}!{clb_name}!{value}!{percent}', 'Назад': f'rep2!{clb_name}',}

    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=str_answer, reply_markup=keyboard)
    await clb.answer()




@router.callback_query(F.data.startswith('rep4'))
async def rep4(clb: CallbackQuery):
    logging.info(f'rep4 -- callback_data = {clb.data}') # rep4!dress_reinforced!1!23'
    tg_id = clb.message.chat.id


    prefix = clb.data.split('!')[-5]
    flag = True if clb.data.split('!')[-4] == 'True' else False
    clb_name = clb.data.split('!')[-3]
    value = clb.data.split('!')[-2]
    percent = int(clb.data.split('!')[-1])
    kristals = (await rq.get_user_dict(tg_id))['kristals']

    bio = (await rq.get_StorageBIO(tg_id))['bio']
    logging.info(f'bio = {bio}')
    xp = await hf.change_xp_percent_and_back(name_thing=clb_name, percent=percent)

    if flag: # если хватает трэша и био для починки (у _kosmonavt и G17  при проверок на flag не было)
        logging.info(f'if flag --- flag={flag}')
        if percent > 50: # для починки используется только био
            logging.info(f'if percent > 50 --- percent={percent}')
            await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][0][1])
            new_xp = xp + dict_repair[clb_name][0][0]

        elif percent <=50: # для починки используется и трэш и био и тут есть _kosmonavt и G17
            logging.info(f'if percent <= 50 --- percent={percent}')
            trash = await rq.get_StorageTrash(tg_id)

            if 'wanderer' in clb_name or clb_name == 'backpack_foliage':
                new_xp = xp + dict_repair[clb_name][1][0]
                await rq.set_storage_trash(tg_id, 'yel_fl', trash['yel_fl'] - dict_repair[clb_name][1][1])
                await rq.set_storage_trash(tg_id, 'stick', trash['stick'] - dict_repair[clb_name][1][2])
                await rq.set_storage_trash(tg_id, 'vine_leaves', trash['vine_leaves'] - dict_repair[clb_name][1][3])
                await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][1][4])
                logging.info(f"if 'wanderer' in clb_name or clb_name == 'backpack_foliage': --- new_xp={new_xp}")

            elif 'reinforced' in clb_name or clb_name == 'backpack_leana':
                new_xp = xp + dict_repair[clb_name][1][0]
                await rq.set_storage_trash(tg_id, 'bones', trash['bones'] - dict_repair[clb_name][1][1])
                await rq.set_storage_trash(tg_id, 'veins', trash['veins'] - dict_repair[clb_name][1][2])
                await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][1][3])
                logging.info(f"elif 'reinforced' in clb_name or clb_name == 'backpack_leana': --- new_xp={new_xp}")

            elif clb_name == 'spear':
                new_xp = xp + dict_repair[clb_name][1][0]
                await rq.set_storage_trash(tg_id, 'stick', trash['stick'] - dict_repair[clb_name][1][1])
                await rq.set_storage_trash(tg_id, 'bones', trash['bones'] - dict_repair[clb_name][1][2])
                await rq.set_storage_trash(tg_id, 'veins', trash['veins'] - dict_repair[clb_name][1][3])
                await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][1][4])
                logging.info(f"elif clb_name == 'spear': --- new_xp={new_xp}")

            elif 'kosmonavt' in clb_name: # только второй словарь
                new_xp = xp + dict_repair[clb_name][1][0]
                await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][1][1])
                await rq.set_user(tg_id, 'kristals', kristals - dict_repair[clb_name][1][2])
                logging.info(f"elif 'kosmonavt' in clb_name: --- new_xp={new_xp}")


            elif clb_name == 'G17':  # у G17 три внутренних словаря --- только третий словарь
                new_xp = xp + dict_repair[clb_name][2][0]
                await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][2][1])
                await rq.set_user(tg_id, 'kristals', kristals - dict_repair[clb_name][2][2])
                logging.info(f"elif clb_name == 'G17': --- new_xp={new_xp}")

    else: # if NOT flag --- 2 варианта, или не хватает для починки или это _kosmonavt / G17 and xp > 50%
        logging.info(f'else --- if NOT flag --- flag={flag}')
        if 'kristals' in clb.data: # или kosmonavt ли G17
            if 'without_kristals' in clb.data: #  только с био (1-й список)
                logging.info(f"if 'kristals' in clb.data: --- if 'without_kristals' in clb.data: --- percent={percent}")

                # делаем проверку, хватает ли БИО
                if bio >= dict_repair[clb_name][0][1]:
                    new_xp = xp + dict_repair[clb_name][0][0]
                    await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][0][1])
                else:
                    keyboard = kb.create_in_kb(1, **{'Ок': 'repair'})
                    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
                    await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
                    return


            else: # if NOT 'without_kristals' , т.е. с кристалом и био (1-й или 2-й список) для космонавта и G17 одинаково

                if bio >= dict_repair[clb_name][1][1]:
                    new_xp = xp + dict_repair[clb_name][1][0]
                    await rq.set_storage_bio(tg_id, 'bio', bio - dict_repair[clb_name][1][1])
                    await rq.set_user(tg_id, 'kristals', kristals - dict_repair[clb_name][1][2])
                    logging.info(f"elif clb_name == 'G17': --- new_xp={new_xp}")
                else:
                    keyboard = kb.create_in_kb(1, **{'Ок': 'repair'})
                    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
                    await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
                    return



        else: # не хватает трэша, flag == False

            keyboard = kb.create_in_kb(1, **{'Ок': 'repair'})
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            return


    new_percent = await hf.change_xp_percent_and_back(name_thing=clb_name, xp=new_xp)
    if new_percent > 100:
        new_percent = 100
        new_xp = await hf.change_xp_percent_and_back(name_thing=clb_name, percent=new_percent)

    # старый процент надо вычеркнуть из строки, новый добавить, записать строку в таблицу
    if clb_name in lsw:
        old_str = (await rq.get_StorageWardrobe(tg_id))[clb_name]
    elif clb_name in lsg:
        old_str = (await rq.get_StorageGun(tg_id))[clb_name]
    new_str = await hf.modify_str_to_str_del_choise_percent_and_null(old_str, str(percent))
    new_str = f'{new_str}!{new_percent}'

    logging.info(f"elif clb_name == {clb_name}: --- new_str={new_str} --- --- old_str={old_str}")
    if clb_name in lsw:
        await rq.set_storage_wardrobe(tg_id, clb_name, new_str)
    elif clb_name in lsg:
        await rq.set_storage_gun(tg_id, clb_name, new_str)

    dict_kb = {'Ок': 'repair'}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=f'Вы починили \n{All_Th[clb_name]} {new_percent}% ({new_xp} ХП)', reply_markup=keyboard)
    await clb.answer()