from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputMediaPhoto

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_use_storage_trash as dict_u,
                                list_storage_trash_craft as craft, LEXICON_scribe_wardrobe as LScrWard,
                                dict_percent_xp, )
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf
from database.help_function import Backpack, Location


router = Router()

import logging

class ListWardrobeFSM(StatesGroup):
    state_wardrobe = State()

# ward1 - F.data == ('storage_wardrobe')
@router.callback_query(F.data == 'storage_wardrobe')
async def ward1(clb: CallbackQuery):
    logging.info(f'ward1 -- callback_data = {clb.data}')
    mes_id = clb.message.message_id
    tg_id = clb.message.chat.id

    data_=await rq.get_StorageWardrobe(tg_id=tg_id)


    dict_ = await hf.modify_dict_to_dict_with_count_value(data_)
    logging.info(f'ward1 -- data_ = {data_} ------- \n dict_ = {dict_}')

    # проверям условие, что в хранилище что-то есть
    if not dict_:# если словарь пустой
        logging.info(f'В storage_wardrobe ничего нет')

        dict_kb = {LBut['back']: 'storage'}
        keyboard = kb.create_in_kb(1, **dict_kb)

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N24']))
        await clb.message.edit_caption(caption='У вас ничего нет', reply_markup=keyboard)
        await clb.answer()

    else: # если словарь НЕ пустой
        logging.info(f'Словарь storage_wardrobe не пустой:')
        #await clb.message.answer_photo(photo=ph['N24'])
        keyboard = kb.create_list_in_kb(width=2, dict_= dict_, prefix1= 'scrp1!ward1',
                                        prefix2='ward1', clb_back_str='storage')

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N24']))
        await clb.message.edit_caption(caption='В хранилище находится:', reply_markup=keyboard)
        await clb.answer()

# F.data.startswith('ward1')
@router.callback_query(F.data.startswith('ward1'))
async def ward2(clb: CallbackQuery):
    logging.info(f'ward2 -- callback_data = {clb.data}')
    tg_id = clb.message.chat.id

# пример колбэка: callback_data = ward1!helmet_wanderer!2
    clb_name = clb.data.split('!')[-2]
    data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_wardrobe_things: dict ={}
    for key, value in dict_data.items():
        dict_wardrobe_things.update({f"[{LSW[clb_name]} {value} шт. {key}%]": f"ward2!{clb_name}!{value}!{key}"})
# модифицируем этот словарь в список списков
    list_button_wardrobe: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_wardrobe_things)

    logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button_wardrobe,
        back=0,
        forward=2,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='ward'
    )

    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption='В Хранилище шкаф находится', reply_markup=keyboard)
    await clb.answer()


# >>>>
@router.callback_query(F.data.startswith('ward_forward'))
async def process_forward(clb: CallbackQuery) -> None:
    logging.info(f'process_forward: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    forward = int(clb.data.split('!')[-2]) + 1
    back = forward - 2

    data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_wardrobe_things: dict ={}
    for key, value in dict_data.items():
        dict_wardrobe_things |= {f"[{LSW[clb_name]} {value} шт. {key}%]": f"ward2!{clb_name}!{value}!{key}"}
# модифицируем этот словарь в список списков
    list_button_wardrobe: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_wardrobe_things)

    logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button_wardrobe,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='ward'
    )

    #keyboard = kb.kb_choise_learners(action='delete_learner', list_learners=list_learners, back=back, forward=forward, count=6)
    try:
        await clb.message.edit_caption(caption='В Хранилище шкаф находится', reply_markup=keyboard)

    except:
        await clb.message.edit_caption(caption='В Хранилищe шкаф находится', reply_markup=keyboard)
    await clb.answer()



# <<<<
@router.callback_query(F.data.startswith('ward_back'))
async def process_forward(clb: CallbackQuery) -> None:
    logging.info(f'process_back: {clb.message.chat.id} ----- clb.data = {clb.data}')
    #list_learners = [learner for learner in await rq.get_all_learners()]
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]
    back = int(clb.data.split('!')[-2]) - 1
    forward = back + 2

    data_=await rq.get_StorageWardrobe(tg_id=tg_id) # Модель из словарей. Ключи - clb_name, значения = строка типа "!0!98!44!0"
    str_data = data_[clb_name] # Строка из БД типа "!0!98!44!0"
    dict_data = await hf.modify_str_to_dict(str_data) # модифицируем строку в словарь
    dict_wardrobe_things: dict ={}
    for key, value in dict_data.items():
        dict_wardrobe_things |= {f"[{LSW[clb_name]} {value} шт. {key}%]": f"ward2!{clb_name}!{value}!{key}"}
# модифицируем этот словарь в список списков
    list_button_wardrobe: list = await hf.modify_dict_to_list_of_list_of_2_elements(dict_wardrobe_things)

    logging.info(f"list_button_wardrobe = {list_button_wardrobe}")

    keyboard = kb.create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button=list_button_wardrobe,
        back=back,
        forward=forward,
        count=5,
        clb_name=clb_name,
        clb_button_back='storage',
        prefix_wardrobe='ward'
    )

    #keyboard = kb.kb_choise_learners(action='delete_learner', list_learners=list_learners, back=back, forward=forward, count=6)
    try:
        await clb.message.edit_caption(caption='В Хранилище шкаф находится', reply_markup=keyboard)

    except:
        await clb.message.edit_caption(caption='В Хранилищe шкаф находится', reply_markup=keyboard)
    await clb.answer()





# Хэндлер на нажатие вещи
#   ['[Шлем странника 1 шт. 44%]', 'ward2!helmet_wanderer!1!44']]
@router.callback_query(F.data.startswith('ward2!')) # Можно прийти как с первой страницы кнопок,
#@router.callback_query(F.data.startswith('ward3!'))  # так и со следующих страниц
async def ward3(clb: CallbackQuery):
    logging.info(f'ward3 -- callback_data = {clb.data}')
    tg_id = clb.message.chat.id
    #await clb.message.answer_photo(photo=ph['N10'])
    clb_name=clb.data.split('!')[-3]
    clb_value=clb.data.split('!')[-2]
    clb_percent=clb.data.split('!')[-1]

    kb_dict: dict = {'Положить в рюкзак': f"ward!put_in_backpack!{clb_name}!{clb_value}!{clb_percent}",
                     'Надеть': f"ward!put_on!{clb_name}!{clb_value}!{clb_percent}",
                     'Выкинуть': f"ward!throw_out!{clb_name}!{clb_value}!{clb_percent}",
                     'Назад': "storage_wardrobe", }
                     #'Назад': f"ward!Backback!{clb_name}!{clb_value}!{clb_percent}", }
    keyboard = kb.create_in_kb(width=1, **kb_dict)
    #await clb.message.edit_text(text=f"{LSW[clb_name]} {clb_value}шт. {clb_percent}%", reply_markup=keyboard)
    #картинку менять не надо
    await clb.message.edit_caption(caption=f"{LSW[clb_name]} {clb_value}шт. {clb_percent}%", reply_markup=keyboard)
    await clb.answer()



@router.callback_query(F.data.startswith('ward!'))
async def putinbackpack_puton_throwout(clb: CallbackQuery):
    """В шкафу выбрали вещь, был задан вопрос Куда ее деть? Здесь надевается вещь только в том случае, если такой же не было надето"""
    logging.info(f"putinbackpack_puton_throwout --- clb.data = {clb.data}")
    tg_id = clb.message.chat.id
    clb_action = clb.data.split('!')[-4]
    clb_name = clb.data.split('!')[-3]
    clb_value = clb.data.split('!')[-2]
    clb_percent = clb.data.split('!')[-1]

    clb_name_prefix = clb_name.split('_')[0] # dress_, helmet_, shoes_, backpack_

    # какие вещи надеты (в таблице User)
    data_user = await rq.get_user_dict(tg_id=tg_id) # словарь со всеми полями
    name_value_user = data_user[clb_name_prefix] # строка нужной колонки ( например 'helmet_wanderer!98') ОНА пустая, если в словаре пусто

    if name_value_user and name_value_user != 'no_backpack': # Если в таблице user это поле не пустое и оно не no_backpack
        logging.info(f'clb_name_prefix = {clb_name_prefix} --- str_things_from_table_user = {name_value_user} --- data_from_table_user = {data_user}')
        name_user = name_value_user.split('!')[0] # Эта вещь надета на игрока
        percent_user = name_value_user.split('!')[1] # Эта % вещи, которая надета на игрока
    else:
        name_user = name_value_user # name_user = 'no_backpack' or name_user = '' А еще поле может быть пустым

    data_wardrobe=await rq.get_StorageWardrobe(tg_id)

 # ПОЛОЖИТЬ В РЮКЗАК
    if clb_action == 'put_in_backpack':
        #backpack_put_on = await hf.what_backpack_put_on(tg_id=tg_id)

        # если никакой, то сообщение, что рюкзака нет
        logging.info(f" if clb_action == 'put_in_backpack': ---- name_value_user = {name_value_user}")
        if data_user['backpack'] == 'no_backpack': # если рюкзак не надет
            keyboard = kb.create_in_kb(1, **{'Ok': 'checking_where_avatar_is_located'})
            await clb.message.edit_caption(caption=f"Рюкзак не надет. Класть некуда.", reply_markup=keyboard)
            await clb.answer()

        elif 'backpack_foliage' in data_user['backpack'] or 'backpack_leana' in data_user['backpack']: # если надет какой-то рюкзак

            list_cell = await hf.create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(
                tg_id=tg_id, prefix=f"ward_pb!{clb_name}!{clb_percent}")
            # Пишу функцию, которая из БД делает список list_cell
            keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back=f"ward2!{clb_name}!{clb_value}!{clb_percent}")
            # уменьшаем на 1 ХП рюкзака
            await rq.decrease_xp_put_on_backpack_1(tg_id)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
            await clb.message.edit_caption(caption=f"В какую ячейку кладем?", reply_markup=keyboard)
            await clb.answer()

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
            # в таблицу User в колонку с имененм брони / рюкзака записываю модификацию и проценты (helmet_wonderer!45)
            await rq.set_user(tg_id, clb_name_prefix, current_value=f"{clb_name}!{clb_percent}") # записываю в таблицу User, в строку clb_name строку типа: вещь!% = helmet_wanderer!45
            # для рюкзаков устанавливается ХП в таблицу соответствующего рюкзака
            value = (int(clb_percent)/100)*dict_percent_xp[clb_name]
            if value > 1:
                value = round(value)
            else:
                value = int(value)
            await rq.set_user(
                tg_id=tg_id,
                name_column=f'xp_{clb_name_prefix}',
                current_value=value)
            #if clb_name == Backpack.backpack_foliage: # в таблилу backpack_foliage устанавливается значение нового хп
             #   await rq.set_backpack_foliage(tg_id, 'xp', int(1.5*int(clb_percent)+0.5)) # хп при создании 150
            #elif clb_name == Backpack.backpack_leana:
             #   await rq.set_backpack_leana(tg_id, 'xp', int(1.8*int(clb_percent)+0.5)) # хп при создании 180
            keyboard = kb.create_in_kb(1, **{'Ok': 'start'})
            await clb.message.edit_caption(caption=f"Вы надели {LST[clb_name]} {clb_percent}%", reply_markup=keyboard)
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
                    await clb.message.edit_caption(caption=f"Вы надели {LST[clb_name]} {clb_percent}%"
                                                        f"\nУ вас был надет {LST[name_user]} {percent_user}%"
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
                                        prefix2='tr1', clb_back_str='checking_where_avatar_is_located', backpack_clb_back='backpack')
                    #keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})




                    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
                    await clb.message.edit_caption(caption=f"не вместилось в новый рюкзак ", # жду ответа, или все вещи перемещаем в , или только то, что не вместилось
                                                   reply_markup=keyboard)

### жду ответы на вопросы



            # для других вещей, кроме рюкзаков
            else:
                keyboard = kb.create_in_kb(1, **kb_dict_common)
                if LST[name_user]:
                    await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_user]))
                    await clb.message.edit_caption(caption=f"Вы надели {LST[clb_name]} {clb_percent}%"
                                                        f"\nУ вас был надет {LST[name_user]} {percent_user}%"
                                                        f"\nКуда его деть?", reply_markup=keyboard)


# ВЫКИНУТЬ
    elif clb_action == 'throw_out':

        new_str_for_wardrobe=await hf.modify_str_to_str_del_choise_percent_and_null(
                str_from_database=data_wardrobe[clb_name],
                choise_percent=clb_percent)
        await rq.set_storage_wardrobe(tg_id, clb_name, new_str_for_wardrobe)
        logging.info(f"ВРЕМЕННО --   elif clb_action == 'throw_out': - new_str_for_wardrobe = {new_str_for_wardrobe}")
        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})
        await clb.message.edit_caption(caption=f"Вы выкинули {LST[clb_name]} {clb_percent}%", reply_markup=keyboard)
        #await clb.answer(text=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name], show_alert=True)



 #
@router.callback_query(F.data.startswith('ward_yet_put_on!'))
async def putinbackpack_putinwardrobe_throwout(clb: CallbackQuery):
    """
    Надевание вещи в этом хэндлере. Если НАДЕЛИ вещь и ТАКАЯ же категория вещи была надета. Здесь показано, что с ней делаем.
    """
    logging.info(f"putinbackpack_putinwardrobe_throwout --- clb.data = {clb.data}")

    tg_id = clb.message.chat.id
    clb_action = clb.data.split('!')[-4]
    clb_name = clb.data.split('!')[-3]
    clb_value = clb.data.split('!')[-2]
    clb_percent = clb.data.split('!')[-1]

    clb_name_prefix = clb_name.split('_')[0] # dress_, helmet_, shoes_, backpack_

    data_wardrobe = await rq.get_StorageWardrobe(tg_id=tg_id)
    data_user = await rq.get_user_dict(tg_id=tg_id)
    name_user_table = data_user[clb_name_prefix].split('!')[-0] # helmet_wanderer!98 <- выбрали helmet_wanderer
    percent_user_table = data_user[clb_name_prefix].split('!')[-1] # helmet_wanderer!98 <- выбрали 98%
    #logging.info(f"ВРЕМЕННО 2 ---- ")



# ПОЛОЖИТЬ В РЮКЗАК + работает, только ХП вещей не одно и теже, что их ### ДУМАЙ, как сделать
    if clb_action == 'put_in_backpack':
        backpack_put_on = await hf.what_backpack_put_on(tg_id=tg_id)

        # если никакой, то сообщение, что рюкзака нет
        if backpack_put_on == 'no_backpack':
            keyboard = kb.create_in_kb(1, **{'Ok': 'checking_where_avatar_is_located'})
            await clb.message.edit_caption(caption=f"Рюкзак не надет. Класть некуда.", reply_markup=keyboard)
            await clb.answer()

        elif backpack_put_on in [Backpack.backpack_foliage, Backpack.backpack_leana]:
            # установка в таблицу Юзер значения из Шкафа
            #await rq.set_user(tg_id=tg_id, name_column=clb_name_prefix, current_value=f"{clb_name}!{clb_percent}") # новое значение в User
            list_cell = await hf.create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(
                tg_id=tg_id, prefix=f"ward_pb_poU!{clb_name}!{clb_percent}") # этот колбэк для случая если надевают вещь из wardrobe, она была надета и ее кладут в рюкзак
            # Пишу функцию, которая из БД делает список list_cell
            keyboard = kb.create_keyboard_from_colored_cell(list_cell=list_cell, clb_back='storage')

            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
            await clb.message.edit_caption(caption=f"В какую ячейку кладем?", reply_markup=keyboard)
            await clb.answer()
            # по итогу: из юзера не убралось. из вардробе убралось. в рюкзак добавилось, но не то

# ПОЛОЖИТЬ В ШКАФ проверить
    elif clb_action == 'put_in_wardrobe':
        if 'backpack' in clb_name:
            dict_backpack = await hf.dict_with_all_things_from_backpack(tg_id=tg_id) # словарь всего того, что есть в рюкзаке
            await hf.delete_all_things_from_put_on_backpack(tg_id) # в надетом рюкзаке удаляет все вещи из всех ячеек
            await hf.put_in_backpack_things_from_dict(tg_id, dict_backpack, clb_name)  # На вход подается словарь. Вещи из словаря кладутся в лиственный рюкзак


        #1  из wardrobe удалить значение, которое надевают, для этого удаляем из строки wardrobe выбранный процент вещи. Он в clb
        new_str_put_on = await hf.modify_str_to_str_del_choise_percent_and_null(data_wardrobe[clb_name], str(clb_percent))
        await rq.set_storage_wardrobe(tg_id, clb_name, new_str_put_on)
        # logging.info(f'1 backpack_leana = {(await rq.get_StorageWardrobe(tg_id))["backpack_leana"]}')

        #2 из таблицы user переложить в таблицу wardrobe
        str_put_off = (await rq.get_StorageWardrobe(tg_id))[name_user_table]
        await rq.set_storage_wardrobe(tg_id, name_user_table, str_put_off+"!"+percent_user_table)
        # logging.info(f'2 backpack_leana = {(await rq.get_StorageWardrobe(tg_id))["backpack_leana"]}')

        #3 надеть то, что пришло в колбэке -> записать в таблицу user
        await rq.set_user(tg_id, clb_name_prefix, clb_name+"!"+clb_percent)

        # установить ХП
        value = (int(clb_percent)/100)*dict_percent_xp[clb_name]
        if value > 1:
            value = round(value)
        else:
            value = int(value)
        await rq.set_user(tg_id=tg_id, name_column=f'xp_{clb_name_prefix}', current_value=value)

        logging.info(f'clb_name = {clb_name} --- clb_percent = {clb_percent} --- name_user_table = {name_user_table} --- percent_user_table = {percent_user_table}')



        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[name_user_table]))
        await clb.message.edit_caption(caption=f"Вы положили в шкаф {LST[name_user_table]} {percent_user_table}% ", reply_markup=keyboard)
        #await clb.answer(text=f"{(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name]}\n"
        #                          f"{(await rq.get_user_dict(tg_id=tg_id))['helmet']}\n"
        #                          f"{(await rq.get_user_dict(tg_id=tg_id))['dress']}\n"
        #                          f"{(await rq.get_user_dict(tg_id=tg_id))['shoes']}\n"
        #                          , show_alert=True)

# ВЫКИНУТЬ + работает
    elif clb_action == 'throw_out':
        # если пришли сюда из рюкзаков, то
        # 1 из старого рюкзака кладем в новый рюкзак вещи (по логике они должны поместиться)
        # 2 в старом рюкзаке зануляем ячейки
        if 'backpack' in clb.data:
            dict_backpack = await hf.dict_with_all_things_from_backpack(tg_id=tg_id) # словарь всего того, что есть в рюкзаке
            await hf.delete_all_things_from_put_on_backpack(tg_id) # в надетом рюкзаке удаляет все вещи из всех ячеек
            await hf.put_in_backpack_things_from_dict(tg_id, dict_backpack, clb_name)  # На вход подается словарь. Вещи из словаря кладутся в рюкзак


        # из wardrobe удалить значение, которое надевают, для этого удаляем из строки wardrobe выбранный процент вещи
        new_str_for_wardrobe=await hf.modify_str_to_str_del_choise_percent_and_null(
                str_from_database=(await rq.get_StorageWardrobe(tg_id))[clb_name],
                choise_percent=clb_percent)
        await rq.set_storage_wardrobe(tg_id, clb_name, new_str_for_wardrobe)
        # надеть то, что пришло в колбэке -> записать в таблицу user
        await rq.set_user(tg_id=tg_id, name_column=clb_name_prefix, current_value=f"{clb_name}!{clb_percent}")
        # записать новый ХП


        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'})
        await clb.message.edit_caption(caption=f"Вы выкинули {LST[name_user_table]} {percent_user_table}%", reply_markup=keyboard)
        #await clb.answer(text=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name], show_alert=True)
        logging.info(f'clb_name={clb_name} --- clb_percent={clb_percent} --- name_user_table={name_user_table} --- percent_user_table={percent_user_table}')



@router.callback_query(F.data.startswith('ward_pb'))
async def ward_put_on_backpack(clb: CallbackQuery):
    """
    Обрабатываются нажатия на цветные ячейки. Тут отдельное условие для случая, когда надевают вещь, которая была уже надета на игрока, и ее убирают в рюкзак
    """
    logging.info(f"ward_put_on_backpack --- clb.data = {clb.data} --- len(clb.data) = {len(clb.data)}")

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-5]
    clb_percent = clb.data.split('!')[-4]
    clb_color_cell = clb.data.split('!')[-3]
    clb_backpack = clb.data.split('!')[-2]
    clb_number_cell = clb.data.split('!')[-1]



    if clb_color_cell == 'red':
        keyboard = kb.create_in_kb(1, **{'Назад': f"ward!put_in_backpack!{clb_name}!{1}!{clb_percent}"}) # Опять попаду сюда???
        logging.info(f' Опять попаду сюда??? clb.data = {clb.data}')
        #ward!put_in_backpack!helmet_reinforced!1!7
        #ward_!helmet_reinforced!7!red!backpack_leana!cell_ 2

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption=f"Сюда положить нельзя", reply_markup=keyboard)
        await clb.answer()

    elif clb_color_cell == 'green':

        keyboard = kb.create_in_kb(1, **{'ok': 'checking_where_avatar_is_located'}) # Проверка где находится аватар???

        # Тут отдельное условие для случая, когда надевают вещь, которая была уже надета на игрока, и ее убирают в рюкзак
        if 'ward_pb_poU' in clb.data: # вещь эже была надета

            if 'backpack' in clb.data:
                dict_backpack = await hf.dict_with_all_things_from_backpack(tg_id=tg_id) # словарь всего того, что есть в рюкзаке
                await hf.delete_all_things_from_put_on_backpack(tg_id) # в надетом рюкзаке удаляет все вещи из всех ячеек
                await hf.put_in_backpack_things_from_dict(tg_id, dict_backpack, clb_name)  # На вход подается словарь. Вещи из словаря кладутся в рюкзак

            data_User = await rq.get_user_dict(tg_id) # 1. Формируе словарь data_User из значений таблицы User: эта вещь была надета, теперь ее надо положить в рюкзак

            name_prefix = clb_name.split('_')[0] if '_' in clb_name else 'houston_we_have_a_problem'
            await rq.set_user(tg_id, name_prefix, clb_name+'!'+clb_percent) # 2 Устанавливаем в таблицу User новые значения: надеваем ту вещь, которая пришла с колбэком (это из wardrobe)

            data_st_w = await rq.get_StorageWardrobe(tg_id=tg_id) # 3 Устанавливаем в wardrobe модифицированную строку. clb_percent по-прежнему из колбэка
            str_from_data_base = data_st_w[clb_name]
            new_str_for_wardrobe = await hf.modify_str_to_str_del_choise_percent_and_null(str_from_database=str_from_data_base, choise_percent=clb_percent)
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column=clb_name, current_value=new_str_for_wardrobe)

            clb_name = data_User[name_prefix].split('!')[0] # 4 переопределяем значения  clb_name и clb_percent. Они должны быть из таблицы User
            clb_percent = data_User[name_prefix].split('!')[1]

            await rq.set_backpack_and_cell_with_chek_put_on_backpack( # 4 устанавливаем в рюкзак переопределенные значения  clb_name и clb_percent. Они должны быть из таблицы User
                tg_id=tg_id,
                cell=clb_number_cell,
                name_column_cell=clb_name,
                current_value_cell=clb_percent
            )

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption=f"Вы положили {LST[clb_name]} {clb_percent}%"
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
        data_st_w = await rq.get_StorageWardrobe(tg_id=tg_id)
        str_from_data_base = data_st_w[clb_name]
        new_str_for_wardrobe = await hf.modify_str_to_str_del_choise_percent_and_null(str_from_database=str_from_data_base, choise_percent=clb_percent)
        await rq.set_storage_wardrobe(tg_id=tg_id, name_column=clb_name, current_value=new_str_for_wardrobe)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"Вы положили {LST[clb_name]} {clb_percent}%"
                                       f"\nв {LBut[clb_number_cell.upper()]}",
                                       reply_markup=keyboard)
        await clb.answer()




@router.callback_query(F.data.startswith('function_what_remaind_things'))
async def function_what_remaind_things(clb: CallbackQuery):
    """
    Запускается функция, которая берет словарь по ключу temp_dict из словаря состояния и переводит его в кнопки
    """
    logging.info(f"function_what_remaind_things --- clb.data = {clb.data} --- len(clb.data) = {len(clb.data)}")
