from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputMediaPhoto

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut, LEXICON_ALL_THINGS as All_Th,
                                dict_percent_xp,
                                )
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf
from database.help_function import Backpack, Location


router = Router()

import logging


# gun1 - F.data == ('storage_wardrobe')
@router.callback_query(F.data == 'storage_gun')
async def gun1(clb: CallbackQuery):
    logging.info(f'gun1 -- callback_data = {clb.data}')

    tg_id = clb.message.chat.id

    data_=await rq.get_StorageGun(tg_id=tg_id)


    dict_ = await hf.modify_dict_to_dict_with_count_value(data_)
    logging.info(f'gun1 -- data_ = {data_} ------- \n dict_ = {dict_}')

    # проверям условие, что в хранилище что-то есть
    if not dict_:# если словарь пустой
        logging.info(f'В storage_gun ничего нет')

        dict_kb = {'Назад': 'storage'}
        keyboard = kb.create_in_kb(1, **dict_kb)

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N39']))
        await clb.message.edit_caption(caption='У вас нет оружия', reply_markup=keyboard)
        await clb.answer()

    else: # если словарь НЕ пустой
        logging.info(f'Словарь storage_gun не пустой:')
        keyboard = kb.create_list_in_kb(width=2, dict_= dict_, prefix1= 'scrp1!st_gun',
                                        prefix2='gun1', clb_back_str='storage')

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N39']))
        await clb.message.edit_caption(caption='В хранилище находится:', reply_markup=keyboard)
        await clb.answer()



# F.data.startswith('gun')
@router.callback_query(F.data.startswith('gun1'))
async def gun2(clb: CallbackQuery):
    logging.info(f'gun2 -- callback_data = {clb.data}')
    tg_id = clb.message.chat.id

# пример колбэка: callback_data = ward1!helmet_wanderer!2
    clb_name = clb.data.split('!')[-2]
    data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things[f"[{All_Th[clb_name]} {value} шт. {key}%]"] = f"gun2!{clb_name}!{value}!{key}"
# модифицируем этот словарь в список списков
    list_button: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    logging.info(f"list_button = {list_button}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button,
        back=0,
        forward=2,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='gun'
    )

    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption='В Хранилище оружия нахидится:', reply_markup=keyboard)
    await clb.answer()


# >>>>
@router.callback_query(F.data.startswith('gun_forward'))
async def process_forward_gun(clb: CallbackQuery) -> None:
    logging.info(f'process_forward_gun: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    forward = int(clb.data.split('!')[-2]) + 1
    back = forward - 2

    data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things |= {f"[{All_Th[clb_name]} {value} шт. {key}%]": f"gun2!{clb_name}!{value}!{key}"}
# модифицируем этот словарь в список списков
    list_gun: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    logging.info(f"list_gun = {list_gun}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_gun,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='gun'
    )

    #keyboard = kb.kb_choise_learners(action='delete_learner', list_learners=list_learners, back=back, forward=forward, count=6)
    try:
        await clb.message.edit_caption(caption='В Хранилище оружия находится', reply_markup=keyboard)

    except:
        await clb.message.edit_caption(caption='В Хранилищe oружия находится', reply_markup=keyboard)
    await clb.answer()



# <<<<
@router.callback_query(F.data.startswith('gun_back'))
async def process_forward_gun(clb: CallbackQuery) -> None:
    logging.info(f'process_back: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    back = int(clb.data.split('!')[-2]) - 1
    forward = back + 2

    data_=await rq.get_StorageGun(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_things: dict ={}
    for key, value in dict_data.items():
        dict_things |= {f"[{All_Th[clb_name]} {value} шт. {key}%]": f"gun2!{clb_name}!{value}!{key}"}
# модифицируем этот словарь в список списков
    list_gun: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_things)

    logging.info(f"list_gun = {list_gun}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_gun,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='gun'
    )

    #keyboard = kb.kb_choise_learners(action='delete_learner', list_learners=list_learners, back=back, forward=forward, count=6)
    try:
        await clb.message.edit_caption(caption='В Хранилище оружия находится', reply_markup=keyboard)

    except:
        await clb.message.edit_caption(caption='В Хранилищe оружия находится', reply_markup=keyboard)
    await clb.answer()




# Хэндлер на нажатие вещи
#   [[Заточенное копье 1 шт. 91%], 'gun2!spear!1!91']
@router.callback_query(F.data.startswith('gun2'))
async def gun3(clb: CallbackQuery):
    logging.info(f'gun3 -- callback_data = {clb.data}')
    tg_id = clb.message.chat.id
    #await clb.message.answer_photo(photo=ph['N10'])
    clb_name=clb.data.split('!')[-3]
    clb_value=clb.data.split('!')[-2]
    clb_percent=clb.data.split('!')[-1]

    kb_dict: dict = {'Положить в рюкзак': f"gun3!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}",
                     'Взять': f"gun3!take_on!{clb_name}!{clb_value}!{clb_percent}",
                     'Выкинуть': f"gun3!throw_out!{clb_name}!{clb_value}!{clb_percent}",
                     'Назад': "storage_gun", }

    keyboard = kb.create_in_kb(width=1, **kb_dict)
    #await clb.message.edit_text(text=f"{LSW[clb_name]} {clb_value}шт. {clb_percent}%", reply_markup=keyboard)
    #картинку менять не надо
    await clb.message.edit_caption(caption=f"{All_Th[clb_name]} {clb_value}шт. {clb_percent}%", reply_markup=keyboard)
    await clb.answer()






@router.callback_query(F.data.startswith('gun3!'))
async def gun4(clb: CallbackQuery):
    """В оружейке выбрали вещь, был задан вопрос Куда ее деть? Здесь надевается вещь только в том случае, если такой же не было надето"""
    logging.info(f"gun4 --- clb.data = {clb.data}")
    # gun3!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}
    tg_id = clb.message.chat.id
    clb_action = clb.data.split('!')[-4]
    clb_name = clb.data.split('!')[-3]
    clb_value = clb.data.split('!')[-2]
    clb_percent = clb.data.split('!')[-1]

    #clb_name_prefix = clb_name.split('_')[0] # dress_, helmet_, shoes_, backpack_

    # какое оружие в руках (в таблице User)
    data_user = await rq.get_user_dict(tg_id=tg_id) # словарь со всеми полями
    left_hand = data_user['left_hand']
    right_hand = data_user['right_hand']
    if left_hand:
        left_hand_gun = left_hand.split('!')[0]
        left_hand_percent = left_hand.split('!')[1]
    if right_hand:
        right_hand_gun = right_hand.split('!')[0]
        right_hand_percent = right_hand.split('!')[1]

    #if name_value_user and name_value_user != 'no_backpack': # Если в таблице user это поле не пустое и оно не no_backpack
     #   logging.info(f'clb_name_prefix = {clb_name_prefix} --- str_things_from_table_user = {name_value_user} --- data_from_table_user = {data_user}')
      #  name_user = name_value_user.split('!')[0] # Эта вещь надета на игрока
       # percent_user = name_value_user.split('!')[1] # Эта % вещи, которая надета на игрока
    #else:
     #   name_user = name_value_user # name_user = 'no_backpack' or name_user = '' А еще поле может быть пустым

    data_gun=await rq.get_StorageGun(tg_id)

 # ПОЛОЖИТЬ В РЮКЗАК
    if clb_action == 'put_in_backpack':
        #backpack_put_on = await hf.what_backpack_put_on(tg_id=tg_id)

        # если никакой, то сообщение, что рюкзака нет
        #logging.info(f'name_value_user = {name_value_user}')
        if data_user['backpack'] == 'no_backpack': # если рюкзак не надет
            keyboard = kb.create_in_kb(1, **{'Ok': 'checking_where_avatar_is_located'})
            await clb.message.edit_caption(caption=f"Рюкзак не надет. Класть некуда.", reply_markup=keyboard)
            await clb.answer()

        elif 'backpack_foliage' in data_user['backpack'] or 'backpack_leana' in data_user['backpack']: # если надет какой-то рюкзак

            list_cell = await hf.create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(
                tg_id=tg_id, prefix=f"gun_pb!{clb_name}!{clb_percent}")
            # Пишу функцию, которая из БД делает список list_cell
            keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back=f"gun2!{clb_name}!{clb_value}!{clb_percent}")

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
            await clb.message.edit_caption(caption=f"В какую ячейку кладем?", reply_markup=keyboard)
            await clb.answer()
# ВЫКИНУТЬ +
    elif clb_action == 'throw_out':

        new_str_for_gun=await hf.modify_str_to_str_del_choise_percent_and_null(
                str_from_database=data_gun[clb_name],
                choise_percent=clb_percent)
        await rq.set_storage_gun(tg_id, clb_name, new_str_for_gun)
        logging.info(f"ВРЕМЕННО --   elif clb_action == 'throw_out': - new_str_for_gun = {new_str_for_gun}")
        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})
        await clb.message.edit_caption(caption=f"Вы выкинули {All_Th[clb_name]} {clb_percent}%", reply_markup=keyboard)
        #await clb.answer(text=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name], show_alert=True)

# ВЗЯТЬ    'Взять': f"gun3!take_on!{clb_name}!{clb_value}!{clb_percent}",
    elif clb_action == 'take_on': # Перекладывать из оружейной будем в других хендлерах

        #new_str_for_gun=await hf.modify_str_to_str_del_choise_percent_and_null(
         #       str_from_database=data_gun[clb_name],
          #      choise_percent=clb_percent)
        #await rq.set_storage_gun(tg_id, clb_name, new_str_for_gun)
        #logging.info(f"ВРЕМЕННО --   elif clb_action == 'throw_out': - new_str_for_gun = {new_str_for_gun}")
        kb_dict = {'Левую': f"gun_take_on!left!{clb_name}!{clb_value}!{clb_percent}",
                   'Правую': f"gun_take_on!right!{clb_name}!{clb_value}!{clb_percent}",
                   'Назад': f'gun2!{clb_name}!{clb_value}!{clb_percent}'} #   [[Заточенное копье 1 шт. 91%], 'gun2!spear!1!91']}
        keyboard = kb.create_in_kb(2, **kb_dict)
        await clb.message.edit_caption(caption=f"В какую руку берем {All_Th[clb_name]} {clb_percent}%", reply_markup=keyboard)






# kb_dict = {'Левую': f"gun_take_on!left!{clb_name}!{clb_value}!{clb_percent}",
@router.callback_query(F.data.startswith('gun_take_on'))
async def gun_take_on(clb: CallbackQuery):
    """
    Проверяется если оружие в этой руке, если есть, то спрашиваем куда его деть [Положить в рюкзак, положить в оружейную, выкинуть]
    и это в следующих хендлерах, если в руке пусто, то кладем в руку
    """
    logging.info(f"gun_take_on --- clb.data = {clb.data} --- len(clb.data) = {len(clb.data)}")

    tg_id = clb.message.chat.id
    clb_hand = clb.data.split('!')[-4]
    clb_name = clb.data.split('!')[-3]
    clb_value = clb.data.split('!')[-2]
    clb_percent = clb.data.split('!')[-1]

    data_user = await rq.get_user_dict(tg_id)
    left_hand = data_user['left_hand']
    right_hand = data_user['right_hand']
    logging.info(f'left_hand = {left_hand} --- clb_hand == left -- {clb_hand}')
    logging.info(f'right_hand = {right_hand} --- clb_hand == right -- {clb_hand}')
    if left_hand and clb_hand == 'left':
        name_user = left_hand.split('!')[0]
        # перевести актуальные проценты в ХП
        percent_user = left_hand.split('!')[1]

    elif right_hand and clb_hand == 'right':
        name_user = right_hand.split('!')[0]
        percent_user = right_hand.split('!')[1]


    if clb_hand == 'left' and left_hand or clb_name == 'right' and right_hand:
        logging.info(f"gun_take_on --- left_hand = {left_hand} --- right_hand = {right_hand}")
        kb_dict_common = {'Положить в рюкзак': f"gun_yet_take_on!put_in_backpack!{clb_hand}!{clb_name}!{clb_value}!{clb_percent}",
                          'Положить в оружейную': f"gun_yet_take_on!put_in_gun!{clb_hand}!{clb_name}!{clb_value}!{clb_percent}",
                          'Выкинуть': f"gun_yet_take_on!throw_out!{clb_hand}!{clb_name}!{clb_value}!{clb_percent}",
                          'Назад': 'storage_gun'}
                           #'Назад': f"ward2!{clb_name}!{clb_value}!{clb_percent}", } # если здесь нажать назад, то, несмотря на сообщение, что вы надели новую вещь,
                                                                                # пользователя вернет назад без сохранения изменения (эта вещь не будет надета)
        keyboard = kb.create_in_kb(1, **kb_dict_common)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_user]))
        await clb.message.edit_caption(caption=f"Вы взяли {All_Th[clb_name]} {clb_percent}%"
                                                f"\nУ вас был взят {All_Th[name_user]} {percent_user}%"
                                                f"\nКуда его деть?", reply_markup=keyboard)



    else: # если берут оружие в руку, в которой нет ничего
        # 1 в User установить новое значение
        await rq.set_user(tg_id, f'{clb_hand}_hand', f'{clb_name}!{clb_percent}')
        new_xp_gun = (int(clb_percent)*dict_percent_xp[clb_name])/100
        new_xp_gun = round(new_xp_gun) if new_xp_gun >= 1 else int(new_xp_gun)
        logging.info(f'new_xp_gun = {new_xp_gun} --- clb_hand = {clb_hand}')
        await rq.set_user(tg_id, f'xp_{clb_hand}_hand', new_xp_gun)

        # 2 в StorageGun записать новую строку без взятого процента
        str_gun = (await rq.get_StorageGun(tg_id))[clb_name]
        new_str_gun = await hf.modify_str_to_str_del_choise_percent_and_null(str_gun, clb_percent)
        await rq.set_storage_gun(tg_id,clb_name, new_str_gun)
        keyboard = kb.create_in_kb(1, **{'Ok': "storage"})
        await clb.message.edit_caption(caption=f"Вы взяли {All_Th[clb_name]} {clb_percent}% в {All_Th[clb_hand.upper()]}", reply_markup=keyboard)






 #
@router.callback_query(F.data.startswith('gun_yet_take_on!'))
async def gun_yet_take_on(clb: CallbackQuery):
    """
    Берется оружие в руки в этом хэндлере. Если БРАЛИ оружие в руку и в этой же руке уже было оружие. Здесь показано, что с ней делаем.
    """
    logging.info(f"gun_yet_take_on --- clb.data = {clb.data}")

    tg_id = clb.message.chat.id
    clb_action = clb.data.split('!')[-5]
    clb_hand = clb.data.split('!')[-4]
    clb_name = clb.data.split('!')[-3]
    clb_value = clb.data.split('!')[-2]
    clb_percent = clb.data.split('!')[-1]


    data_user = await rq.get_user_dict(tg_id)
    data_user_hand = data_user[f'{clb_hand}_hand'] # то, что лежит в руке (пришло в колбэке)
    name_user = data_user_hand.split('!')[0]
    name_percent = data_user_hand.split('!')[1]

    data_gun = await rq.get_StorageGun(tg_id) # то, что лежит оружейной
    str_gun = data_gun[name_user] # та строка оружейной, оружие которой лежит в выбранной руке

    #kb_dict_common = {'Положить в рюкзак': f"gun_yet_take_on!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}",
     #                 'Положить в оружейную': f"gun_yet_take_on!put_in_storage_gun!{clb_name}!{clb_value}!{clb_percent}",
      #                'Выкинуть': f"gun_yet_take_on!throw_out!{clb_name}!{clb_value}!{clb_percent}",
       #               'Назад': 'storage_gun'}

    # ВЫКИНУТЬ
    if clb_action == 'throw_out':

        #1 из storage_Gun удаляем выбранный процент (пришел в колбэке)
        new_str_for_gun=await hf.modify_str_to_str_del_choise_percent_and_null(
                (await rq.get_StorageGun(tg_id))[clb_name], clb_percent)
        await rq.set_storage_gun(tg_id, clb_name, new_str_for_gun)
        #if clb_name==name_user:

        #2 в User установить
        await rq.set_user(tg_id, f'{clb_hand}_hand', f'{clb_name}!{clb_percent}')
        new_xp_gun = (int(clb_percent)*dict_percent_xp[clb_name])/100
        new_xp_gun = round(new_xp_gun) if new_xp_gun >= 1 else int(new_xp_gun)
        logging.info(f'new_xp_gun = {new_xp_gun} --- clb_hand = {clb_hand}')
        await rq.set_user(tg_id, f'xp_{clb_hand}_hand', new_xp_gun)

        #else:

            #2 к этой строке прибавляем процент из data_user
            #new_str_for_gun+=f'!{name_percent}'

        #await rq.set_storage_gun(tg_id, clb_name, new_str_for_gun)
        logging.info(f"ВРЕМЕННО --   elif clb_action == 'throw_out': - new_str_for_gun = {new_str_for_gun}")
        keyboard = kb.create_in_kb(1, **{'ok': 'storage'})
        await clb.message.edit_caption(caption=f"Вы выкинули {All_Th[name_user]} {name_percent}%", reply_markup=keyboard)
        #await clb.answer(text=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name], show_alert=True)

    # ПОЛОЖИТЬ В ОРУЖЕЙНУЮ  # работает
    elif clb_action == 'put_in_gun':
        #1 из storage_Gun удаляем выбранный процент (пришел в колбэке)
        new_str_for_gun=await hf.modify_str_to_str_del_choise_percent_and_null(
                str_from_database=data_gun[clb_name],
                choise_percent=clb_percent)
        await rq.set_storage_gun(tg_id, clb_name, new_str_for_gun)
        #logging.info(f"ВРЕМЕННО ПЕРВАЯ --   elif clb_action == 'put_in_gun': - new_str_for_gun = {new_str_for_gun}")
        #2 в User установить
        await rq.set_user(tg_id, f'{clb_hand}_hand', f'{clb_name}!{clb_percent}')
        new_xp_gun = (int(clb_percent)*dict_percent_xp[clb_name])/100
        new_xp_gun = round(new_xp_gun) if new_xp_gun >= 1 else int(new_xp_gun)
        logging.info(f'new_xp_gun = {new_xp_gun} --- clb_hand = {clb_hand}')
        await rq.set_user(tg_id, f'xp_{clb_hand}_hand', new_xp_gun)

        #3 в оружейную положить то, что лежало в руке
        str_for_gun= data_gun[name_user]
        new_str_for_gun = str_for_gun + '!' + name_percent
        await rq.set_storage_gun(tg_id, name_user, new_str_for_gun)


        #logging.info(f"ВРЕМЕННО ВТОРАЯ --   elif clb_action == 'put_in_gun': - new_str_for_gun = {new_str_for_gun}")
        keyboard = kb.create_in_kb(1, **{'ok': 'storage'})
        await clb.message.edit_caption(caption=f"Вы положили в оружейную {All_Th[name_user]} {name_percent}%", reply_markup=keyboard)
        #await clb.answer(text=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name], show_alert=True)

    elif clb_action == 'put_in_backpack':
        logging.info(f"ВРЕМЕННО 416 --   elif clb_action == 'put_in_backpack': data_user = {data_user}")

        #backpack_put_on = await hf.what_backpack_put_on(tg_id=tg_id)

        # если никакой, то сообщение, что рюкзака нет
        #logging.info(f'name_value_user = {name_value_user}')
        if data_user['backpack'] == 'no_backpack': # если рюкзак не надет
            keyboard = kb.create_in_kb(1, **{'Ok': 'checking_where_avatar_is_located'})
            await clb.message.edit_caption(caption=f"Рюкзак не надет. Класть некуда.", reply_markup=keyboard)
            await clb.answer()

        elif 'backpack_foliage' in data_user['backpack'] or 'backpack_leana' in data_user['backpack']: # если надет какой-то рюкзак

            list_cell = await hf.create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(
                tg_id=tg_id, prefix=f"gun_pb_poU!{clb_hand}!{clb_name}!{clb_percent}")
            # Пишу функцию, которая из БД делает список list_cell
            keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back=f"gun2!{clb_name}!{clb_value}!{clb_percent}")

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
            await clb.message.edit_caption(caption=f"В какую ячейку кладем?", reply_markup=keyboard)
            await clb.answer()




@router.callback_query(F.data.startswith('gun_pb'))
async def gun_put_on_backpack(clb: CallbackQuery):
    """
    Обрабатываются нажатия на цветные ячейки. Тут отдельное условие для случая, когда надевают вещь, которая была уже надета на игрока, и ее убирают в рюкзак
    """
    logging.info(f"gun_put_on_backpack --- clb.data = {clb.data} --- len(clb.data) = {len(clb.data)}")

    tg_id = clb.message.chat.id
    clb_hand = clb.data.split('!')[-6]
    clb_name = clb.data.split('!')[-5]
    clb_percent = clb.data.split('!')[-4]
    clb_color_cell = clb.data.split('!')[-3]
    clb_backpack = clb.data.split('!')[-2]
    clb_number_cell = clb.data.split('!')[-1]



    if clb_color_cell == 'red':
        keyboard = kb.create_in_kb(1, **{'Назад': f"gun3!put_in_backpack!{clb_name}!{1}!{clb_percent}"})

        # {'Положить в рюкзак': f"gun3!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}",

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption=f"Сюда положить нельзя", reply_markup=keyboard)
        await clb.answer()

    elif clb_color_cell == 'green':

        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'}) # Проверка где находится аватар???

        # Тут отдельное условие для случая, когда надевают вещь, которая была уже надета на игрока, и ее убирают в рюкзак
        if 'gun_pb_poU' in clb.data: # вещь эже была надета

            #if 'backpack' in clb.data:
             #   dict_backpack = await hf.dict_with_all_things_from_backpack(tg_id=tg_id) # словарь всего того, что есть в рюкзаке
              #  await hf.delete_all_things_from_put_on_backpack(tg_id) # в надетом рюкзаке удаляет все вещи из всех ячеек
               # await hf.put_in_backpack_things_from_dict(tg_id, dict_backpack, clb_name)  # На вход подается словарь. Вещи из словаря кладутся в рюкзак
###########################
            data_User = await rq.get_user_dict(tg_id) # 1. Формируе словарь data_User из значений таблицы User: эта оружие было в руке, теперь его надо положить в рюкзак
            clb_hand = f'{clb_hand}_hand'
            name_user = data_User[clb_hand].split('!')[0]
            percent_user = data_User[clb_hand].split('!')[1] # то что лежит в руке сейчас
            await rq.set_user(tg_id, clb_hand, clb_name+'!'+clb_percent) # 2 Устанавливаем в таблицу User новые значения: берем в руку то оружие, которая пришло с
            new_xp_gun = (int(clb_percent)*dict_percent_xp[clb_name])/100
            new_xp_gun = round(new_xp_gun) if new_xp_gun >= 1 else int(new_xp_gun)
            logging.info(f'new_xp_gun = {new_xp_gun} --- clb_hand = {clb_hand}')
            await rq.set_user(tg_id, f'xp_{clb_hand}', new_xp_gun)

            data_st_gun = await rq.get_StorageGun(tg_id=tg_id) # 3 Устанавливаем в Gun модифицированную строку. clb_percent по-прежнему из колбэка
            str_from_data_base = data_st_gun[clb_name]
            new_str_for_gun = await hf.modify_str_to_str_del_choise_percent_and_null(str_from_database=str_from_data_base, choise_percent=clb_percent)
            await rq.set_storage_gun(tg_id=tg_id, name_column=clb_name, current_value=new_str_for_gun)

           # clb_name = data_User[name_prefix].split('!')[0] # 4 переопределяем значения  clb_name и clb_percent. Они должны быть из таблицы User
           # clb_percent = data_User[name_prefix].split('!')[1]

            await rq.set_backpack_and_cell_with_chek_put_on_backpack( # 4 устанавливаем в рюкзак то, что было в руке
                tg_id=tg_id,
                cell=clb_number_cell,
                name_column_cell=name_user,
                current_value_cell=percent_user
            )

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_user]))
            await clb.message.edit_caption(caption=f"Вы положили {All_Th[name_user]} {percent_user}%"
                                        f"\nв {LBut[clb_number_cell.upper()]}",
                                        reply_markup=keyboard)
            await clb.answer()
            return

        #  ward_put_on_backpack --- clb.data = ward_!backpack_leana!33!green!backpack_foliage!cell_1
        await rq.set_backpack_and_cell_with_chek_put_on_backpack(
            tg_id=tg_id,
            cell=clb_number_cell,
            name_column_cell=clb_name,
            current_value_cell=clb_percent
        )

        #await rq.set_b_leana_cell_3(tg_id=tg_id, name_column=clb_name, current_value=clb_percent)#f"{clb_percent}")
        # эта вещь удаляется из шкафа
        data_st_gun = await rq.get_StorageGun(tg_id=tg_id)
        str_from_data_base = data_st_gun[clb_name]
        new_str_for_gun = await hf.modify_str_to_str_del_choise_percent_and_null(str_from_database=str_from_data_base, choise_percent=clb_percent)
        await rq.set_storage_gun(tg_id=tg_id, name_column=clb_name, current_value=new_str_for_gun)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"Вы положили {All_Th[clb_name]} {clb_percent}%"
                                       f"\nв {LBut[clb_number_cell.upper()]}",
                                       reply_markup=keyboard)
        await clb.answer()







# 'Взять': f"gun3!take_on!{clb_name}!{clb_value}!{clb_percent}",
"""
 # НАДЕТЬ
 # Здесь надевается вещь только в том случае, если такой же не было надето кроме рюкзаков, т.к. у них надо смотреть вещи в ячейках
    elif clb_action == 'put_on': # putinbackpack_puton_throwout --- clb.data = ward!put_on!helmet_reinforced!1!22
        #name_user = clb.data.split("!")[-3] # переопределяем для случая, если ничего не надето
        #clb_percent = clb.data.split("!")[-1]
        if not name_user or name_user == 'no_backpack': # если этот вид одежды/брони/рюкзака НЕ НАДЕТ

            # вычитаю функцией из строки в wardrobe ту вещь, которую я надел
            new_str_for_wardrobe=await hf.modify_str_to_str_del_choise_percent_and_null(
                str_from_database=data_wardrobe[clb_name],
                choise_percent=clb_percent)

            logging.info(f'ВРЕМЕННО ---- new_str_for_wardrobe = {new_str_for_wardrobe} --- {name_user}')
            await rq.set_storage_wardrobe(tg_id, clb_name, new_str_for_wardrobe)
            await rq.set_user(tg_id, clb_name_prefix, current_value=f"{clb_name}!{clb_percent}") # записываю в таблицу User, в строку clb_name строку типа: вещь!% = helmet_wanderer!45
            # для рюкзаков устанавливается ХП в таблицу соответствующего рюкзака
            if clb_name == Backpack.backpack_foliage: # в таблилу backpack_foliage устанавливается значение нового хп
                await rq.set_backpack_foliage(tg_id, 'xp', int(1.5*int(clb_percent)+0.5)) # хп при создании 150
            elif clb_name == Backpack.backpack_leana:
                await rq.set_backpack_leana(tg_id, 'xp', int(1.8*int(clb_percent)+0.5)) # хп при создании 180
            keyboard = kb.create_in_kb(1, **{'Ok': 'start'})
            await clb.message.edit_caption(caption=f"Вы надели {All_Th[clb_name]} {clb_percent}%", reply_markup=keyboard)
            await clb.answer()

        else: # если этот вид одежды/брони/рюкзак УЖЕ НАДЕТ (сделано в следующем колбэке)

            # Этот словарь общий для вещей и рюкзаков при переходе к выбору, что делать с вещаями, когда надевают другое
            kb_dict_common = {'Положить в рюкзак': f"ward_yet_put_on!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}",
                            'Положить в шкаф': f"ward_yet_put_on!put_in_wardrobe!{clb_name}!{clb_value}!{clb_percent}",
                            'Выкинуть': f"ward_yet_put_on!throw_out!{clb_name}!{clb_value}!{clb_percent}",
                            'Назад': 'storage'}
                            #'Назад': f"ward2!{clb_name}!{clb_value}!{clb_percent}", } # если здесь нажать назад, то, несмотря на сообщение, что вы надели новую вещь,
                                                                                    # пользователя вернет назад без сохранения изменения (эта вещь не будет надета)
        #else: если этот вид одежды/брони/рюкзак УЖЕ НАДЕТ (сделано в следующем колбэке)
        # Cперва рюкзаки. Для РЮКЗАКОВ дополнительная проверка
            if name_user in [Backpack.backpack_foliage, Backpack.backpack_leana]: # если был надет рюкзак
                location = data_user['location']
                logging.info(f"ПЕРВЫЙ 282 all_things_can_be_moved_to_a_new_backpack = {await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id)}")


                if await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id):
                # Если все вещи МОГУТ быть перемещены в новый рюкзак, то
                            # 1 спрашиваем куда деть старый
                            #  т.к. в этом вопросе есть кнопка НАЗАД, то
                            #  2 перемещаем эти вещи в новый рюкзак и надеваем новый рюкзак в тех хэндлерах,
                                # куда я перейду с действиями Выбросить, положить в шкаф, положить в рюкзак

                    keyboard = kb.create_in_kb(1, **kb_dict_common)
                    await clb.message.edit_caption(caption=f"Вы надели {All_Th[clb_name]} {clb_percent}%"
                                                        f"\nУ вас был надет {All_Th[name_user]} {percent_user}%"
                                                        f"\nКуда его деть?", reply_markup=keyboard)



                elif not await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id) and location == Location.landing_place:# +
                # Если вещи НЕ МОГУТ быть перемещены в новый рюкзак и находимся в локации Место посадки, то
                # 1.Забиваем лиственный рюкзак, а 2. Оставшиеся вещи перемещаем в соответствующие Хранилища
                    logging.info(f"ВТОРОЙ 300 all_things_can_be_moved_to_a_new_backpack = {await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id)} --- location = {location}")

                    stroka = (await hf.things_put_on_in_backpack_foliage_after_put_on_in_storages(tg_id=tg_id, percent_backpack_foliage=clb_percent))[0]
                    await rq.set_user(tg_id, 'backpack', clb_name+'!'+clb_percent)
                    keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})
                    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
                    await clb.message.edit_caption(caption=f"не вместилось в новый рюкзак "
                                                        f"\n и было перемещено в хранилище\n"
                                                        f"{stroka}", reply_markup=keyboard)# жду ответа, или все вещи перемещаем, или только то, что не вместилось



                elif not await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id) and location != Location.landing_place:
                    logging.info(f"ТРЕТИЙ 326 all_things_can_be_moved_to_a_new_backpack = {await hf.all_things_can_be_moved_to_a_new_backpack(tg_id=tg_id)} --- location = {location}")
                # Если вещи НЕ МОГУТ быть перемещены в новый рюкзак и НЕ находимся в локации Место посадки, то
                    list_return = await hf.things_put_on_in_backpack_foliage_after_put_on_in_storages(tg_id=tg_id, percent_backpack_foliage=clb_percent)
                    stroka = list_return[0]
                    dict_return = list_return[1]

                    await rq.set_user(tg_id, 'backpack', clb_name+'!'+clb_percent)
                    #dict_return['Рюкзак'] = 'backpack'
                    keyboard = kb.create_list_in_kb(width=2, dict_= dict_return, prefix1= 'scrp1!tr1',
                                        prefix2='tr1', clb_back_str='checking_where_avatar_is_located', backpack='backpack')
                    #keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})




                    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
                    await clb.message.edit_caption(caption=f"не вместилось в новый рюкзак ", # жду ответа, или все вещи перемещаем в , или только то, что не вместилось
                                                   reply_markup=keyboard)

### жду ответы на вопросы



            # для других вещей, кроме рюкзаков
            else:
                keyboard = kb.create_in_kb(1, **kb_dict_common)
                if All_Th[name_user]:
                    await clb.message.edit_caption(caption=f"Вы надели {All_Th[clb_name]} {clb_percent}%"
                                                        f"\nУ вас был надет {All_Th[name_user]} {percent_user}%"
                                                        f"\nКуда его деть?", reply_markup=keyboard)

"""
