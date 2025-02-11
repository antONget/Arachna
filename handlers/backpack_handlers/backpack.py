from aiogram import F, Router, Bot

from aiogram.filters import Command, StateFilter
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
from database.help_function import Backpack
#from handlers.location_anather_h.meadows_hunt import MeadowsHuntFSM
#from handlers.location_anather_h.meadows_loot import MeadowsLootFSM


router = Router()

storage = MemoryStorage()

import logging

class LaboratoryFSM(StatesGroup):
    state_save_lb4 = State()

#b1 backpack
# износ рюкзака происходит при каждом с ним взаимодействии.    -1ХП
# в хэндлерах, где уменьшается хп делать проверку "не умер ли аватар", пока заглушка
# можно делать всплывалочку об уменьшении хр
@router.callback_query(F.data == 'backpack')
@router.callback_query(F.data == 'backpack_landing_place')
@router.callback_query(F.data == 'backpack_go_to')
@router.callback_query(F.data == 'backpack_meadows') # backpack_meadows
@router.callback_query(F.data == 'backpack_loot')

async def b1(clb: CallbackQuery):
    tg_id=clb.message.chat.id
    logging.info(f"b1 --- clb.data = {clb.data}")

    backpack = await hf.what_backpack_put_on(tg_id=tg_id) # какой рюкзак надет?

    # вычитаем ХП рюкзака из таблицы USER, если == 0, то запускаем функцию
    #await rq.decrease_xp_put_on_backpack_1(tg_id)
    #current_xp_backpack = (await rq.get_user_dict(tg_id))['xp_backpack']
    #logging.info(f'current_xp_backpack = {current_xp_backpack}')
    #if current_xp_backpack == 0:
     #   await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=backpack)
      #  return



    #if '!' in data_backpack:
    #    backpack = data_backpack.split('!')[0]
    #else:
    #    backpack = data_backpack

    # если пришли сюда из 'backpack_С_ПРИСТАВКОЙ', значит надо в базу данных записать clb_back
    # если пришли сюда из обычного 'backpack', значит надо ИЗ БД взять clb_back
    if clb.data != 'backpack':
        if clb.data == 'backpack_landing_place':
            clb_back = 'checking_where_avatar_is_located'
        elif clb.data == 'backpack_go_to':
            clb_back = 'location_go_to_back'
        elif clb.data == 'backpack_meadows':
            clb_back = 'location_meadows'
        elif clb.data == 'backpack_loot':
            clb_back = 'loot2'#'what_do'
        await rq.set_backpack_foliage(tg_id=tg_id, name_column='clb_back', current_value=clb_back)
    else:
        clb_back = (await rq.get_BackpackFoliage(tg_id))['clb_back']

#class MeadowsLootFSM(StatesGroup):
#    state_meadows1 = State() # F.data == 'location_meadows'
#    state_loot_2 = State() # F.data == 'loot2'



    #if await state.get_state() == MeadowsHuntFSM.state_you_win:
     #   clb_back = 'you_are_win'
    #elif await state.get_state() == MeadowsLootFSM.state_meadows1:
        #clb_back = 'location_meadows'
    #elif await state.get_state() == MeadowsLootFSM.state_loot_2:
     #   clb_back = 'loot2'

    #logging.info(f'state.get_state() = {await state.get_state()}')

    if backpack == Backpack.no_backpack:
        keyboard = await kb.create_kb_show_cells_backpack(tg_id=tg_id, prefix='b2', clb_back=clb_back)

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
        await clb.message.edit_caption(caption='Рюкзак не надет.\nДоступны только карманы.', reply_markup=keyboard)
        await clb.answer()
    elif backpack in [Backpack.backpack_foliage, Backpack.backpack_leana]:

        keyboard = await kb.create_kb_show_cells_backpack(tg_id=tg_id, prefix='b2', clb_back=clb_back)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
        await clb.message.edit_caption(caption='У вас в рюкзаке', reply_markup=keyboard)
        await clb.answer()


    # Какой рюкзак надет
    #await rq.decrease_xp_backpack_1(tg_id=clb.message.chat.id)
    #data_user=await rq.get_BackpackFoliage(tg_id=clb.message.chat.id)

    #fak = await rq.get_BackpackFoliage(tg_id=tg_id)
    #await clb.message.answer_photo(photo=ph['N_1'])
    #dict_kb={LBut['bio_500']: 'bio_500_1', f'Аптечка {fak.f_aid} шт': 'f_aid_3_1',
    #                LBut['empty']: 'empty_1', ' '+LBut['empty']+' ': 'empty_2',
    #                'Пуcто': 'empty_3', LBut['back']: 'start',}
    #keyboard = kb.create_in_kb(2, **dict_kb)
    #await clb.message.answer(text=LB['b1'], reply_markup=keyboard)
    #logging.info(f'b1 fak.xp = {fak.xp}; b1 fak.first_aid kit = {fak.f_aid}')




# @router.callback_query(F.data.startswith('b2'))
@router.callback_query(F.data.startswith('b2'))
async def b2(clb: CallbackQuery, state: FSMContext):
    logging.info(f"b2 --- clb.data = {clb.data} --- len(clb.data.encode('utf-8')) = {len(clb.data.encode('utf-8'))}")
    tg_id = clb.message.chat.id
    location = (await rq.get_user_dict(tg_id=tg_id))['location']

    clb_backpack = clb.data.split('!')[-4]
    clb_pocket_cell = clb.data.split('!')[-3]
    clb_name = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]

    ###  ВРЕМЕННО покажет алерт, если хп < 0
    if (await rq.get_user_dict(tg_id=tg_id))['xp']<0:
        await clb.answer('ХП меньше 0', show_alert=True)

    ### ВНИМАНИЕ, делаем проверку на наличие словаря в state
        # если есть, то колбэк приводит в loot2
    dict_with_loot_from_state = await state.get_data()

    if clb_name == 'clb_for_bio':
        if location == 'landing_place' and int(clb_value)>0: # Если на локации Landing_place БИО есть в рюкзаке
            keyboard = kb.create_in_kb(1, **{'Переложить в хранилище': f"remove_bio_from_backpack_to_storage!{clb_backpack}!{clb_value}",
                                             'Назад': 'backpack'})
        elif location != 'landing_place' and dict_with_loot_from_state:
            keyboard = kb.create_in_kb(1, **{'Назад': 'loot2'})
        else: # на любой другой локации
            keyboard = kb.create_in_kb(1, **{'Назад': 'backpack'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N41']))
        await clb.message.edit_caption(caption=f"У вас в рюкзаке {clb_value} био ", reply_markup=keyboard)
        await clb.answer()

    elif clb_name == 'Пусто':

        if clb_pocket_cell.startswith('cell'): # если взаимодействие с РЮКЗАКОМ - 1 хп
            if not await hf.check_xp_put_on_backpack_if_more_then_zero(tg_id=tg_id): # проваливаемся сюда, если ХП < 0
                # если ХП рюкзака меньше 0, то запускаю функцию  xp_backpack_is_over_remove_things_delate_backpack
                await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=clb_backpack)
                return
            await rq.decrease_xp_put_on_backpack_1(tg_id=tg_id) # уменьшаем ХП, если нажали на рюкзак и ХП > 0

        # если есть, то колбэк приводит в loot2

        if not dict_with_loot_from_state:
            keyboard = kb.create_in_kb(1, **{'Назад': 'backpack'})
        else:
            keyboard = kb.create_in_kb(1, **{'Назад': 'loot2'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption=f"{LBut[clb_pocket_cell]} \nЗдесь ничего нет ", reply_markup=keyboard)
        await clb.answer()


    else: # не био и не Пусто, но тут и Карманы. и Ячейки рюкзаков.
        logging.info(f'else: # не био и не Пусто, но тут и Карманы. и Ячейки рюкзаков. ')

        # ПРОВЕРКА ХП РЮКЗАКА, ЕСЛИ 0, ЗАПУСК УДАЛЕНИЯ И ПЕРЕМЕЩЕНИЯ ВЕЩЕЙ
        ## 1 МЕСТО
        if clb_pocket_cell.startswith('cell'): # если взаимодействие с РЮКЗАКОМ - 1 хп
            logging.info(f"if clb_pocket_cell.startswith('cell'): # если взаимодействие с РЮКЗАКОМ - 1 хп {clb_pocket_cell}")
            if not await hf.check_xp_put_on_backpack_if_more_then_zero(tg_id=tg_id): # проваливаемся сюда, если ХП < 0
                # если ХП рюкзака меньше 0, то запускаю функцию  xp_backpack_is_over_remove_things_delate_backpack
                await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=clb_backpack)
                return
            await rq.decrease_xp_put_on_backpack_1(tg_id=tg_id) # уменьшаем ХП, если нажали на рюкзак и ХП > 0

        ### ВНИМАНИЕ, делаем проверку на наличие словаря в state
        # если есть, то колбэк приводит в loot2
        #dict_with_loot_from_state = await state.get_data()
        if location == 'landing_place':
            dict_kb = {'Положить в хранилище': f'b3!put_in_storage!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Доложить': f'b3!dologit!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Переложить': f'b3!perelogit!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Использовать': f'b3!use!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Выкинуть': f'b3!throw_it_out!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Назад': 'backpack'}
        elif location != 'landing_place': #and not dict_with_loot_from_state:
            dict_kb = {'Переложить': f'b3!perelogit!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Использовать': f'b3!use!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Выкинуть': f'b3!throw_it_out!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Назад': 'backpack'}

        else:
            dict_kb = {'Переложить': f'b3!perelogit!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Использовать': f'b3!use!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Выкинуть': f'b3!throw_it_out!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}',
                    'Назад': 'loot2'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        # x = a if condition else b
        pp = '%' if clb_name in LSWG else 'шт.'
        await clb.message.edit_caption(caption=f"У вас {LST[clb_name]} {clb_value}{pp} \nв {LBut[clb_pocket_cell.capitalize()]} \n\nЧто делаем?", reply_markup=keyboard)
        await clb.answer()


# f"remove_bio_from_backpack_to_storage!{clb_backpack}!{clb_value}
@router.callback_query(F.data.startswith('remove_bio_from_backpack_to_storage'))
async def remove_bio_from_backpack_to_storage(clb: CallbackQuery):
    logging.info(f"remove_bio_from_backpack_to_storage --- clb.data = {clb.data}  --- len(clb.data.encode('utf-8')) = {len(clb.data.encode('utf-8'))}")
    tg_id = clb.message.chat.id

    clb_backpack = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]
    bio_in_storage = (await rq.get_StorageBIO(tg_id=tg_id))['bio']
    await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=int(clb_value)+bio_in_storage)# суммируем био из хранилища и рюкзака
    if clb_backpack == Backpack.backpack_foliage:# установливаем 0 в надетом рюкзаке
        await rq.set_backpack_foliage(tg_id=tg_id, name_column='bio', current_value=0)
    elif clb_backpack == Backpack.backpack_leana:
        await rq.set_backpack_leana(tg_id=tg_id, name_column='bio', current_value=0)

    keyboard = kb.create_in_kb(1, **{'ok': 'backpack'})
    await clb.message.edit_caption(caption=f"У вас в Хранилище Био {int(clb_value)+bio_in_storage} био ресурса", reply_markup=keyboard)
    await clb.answer()





# Формирование клавиатуры в зависимости от --- 1. ДЕЙСТВИЯ (Положить в хранилище, Доложить, Переложить, Использовать, Выкинуть)
#                                              2. КОЛИЧЕСВА ВЕЩЕЙ из рюкзака,
#                                              3. КОЛИЧЕСВА ВЕЩЕЙ из Хранилища,
@router.callback_query(F.data.startswith('b3!')) # для апробации клавиатуры делам только выкинуть
async def b3_prepare_action(clb: CallbackQuery):
    logging.info(f"b3! --- clb.data = {clb.data}  --- len(clb.data.encode('utf-8')) = {len(clb.data.encode('utf-8'))}")
    tg_id = clb.message.chat.id

    clb_action = clb.data.split('!')[-5]
    clb_backpack = clb.data.split('!')[-4]
    clb_pocket_cell = clb.data.split('!')[-3]
    clb_name = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]

    if clb_name in list_storage_trash:
        value_storage = (await rq.get_StorageTrash(tg_id=tg_id))[clb_name]
    else:
        value_storage=0 ### непонятная заглушка


    #if clb_name in LSWG:
    #    clb_value = 1 # и пускай в клавиатуре будет

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N25']))

# ПОЛОЖИТЬ В ХРАНИЛИЩЕ
    if clb_action=='put_in_storage':
        logging.info(f"b3! --- if clb_action == put_in_storage")
        keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(tg_id=tg_id, prefix='b4',
                                                                   value_pocket_cell=int(clb_value),
                                                                   value_storage=value_storage,
                                                                   clb_action=clb_action,
                                                                   clb_backpack=clb_backpack,
                                                                   clb_pocket_cell=clb_pocket_cell,
                                                                   clb_name=clb_name,
                                                                   clb_back='backpack'
                                                                   )
        if clb_name in list_storage_trash:
            pp = 'шт.'
        else:
            pp = '%'
        await clb.message.edit_caption(caption=
                                       f"У вас {All_Th[clb_name]} {clb_value}{pp}\nСколько положить в хранилище?",
                                       reply_markup=keyboard) # клавиатура сделана в kb

# ДОЛОЖИТЬ
    elif clb_action=='dologit':
        logging.info(f"b3! --- if clb_action == dologit")
        if clb_name in list_storage_trash: # в зависимости от того, что лежит в ячейке узнаем, есть ли эта вещь в хранилище Трэш
            data_storage=(await rq.get_StorageTrash(tg_id=tg_id))[clb_name]

            logging.info(f"b3! --- if clb_action == dologit --- data_storage = {data_storage}")

            if data_storage: # Если в хранилище ТРЭШ есть эта вещь
                if int(clb_value)==20: # если нет свободного места
                    keyboard_loc = kb.create_in_kb(1, **{'ok': 'backpack'})
                    await clb.message.edit_caption(caption=
                                                    f"У вас в {LBut[clb_pocket_cell.capitalize()]}\n"
                                                    f"нет свободного места.\n"
                                                    f"Доложить ничего нельзя.",
                                                    reply_markup=keyboard_loc)

                else: # в ячейке/кармане есть свободное место
                    keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(
                        tg_id=tg_id,
                        prefix='b4',
                        value_pocket_cell=int(clb_value),
                        value_storage=value_storage,
                        clb_action=clb_action,
                        clb_backpack=clb_backpack,
                        clb_pocket_cell=clb_pocket_cell,
                        clb_name=clb_name,
                        clb_back='backpack'
                        )
                    await clb.message.edit_caption(
                        caption=
                        f"У вас в хранилище {data_storage}шт. {All_Th[clb_name]}\n"
                        f"В {LBut[clb_pocket_cell.capitalize()]}"
                        f"{f' свободного места {20-int(clb_value)}'}\n"
                        f"Сколько доложить?",
                        reply_markup=keyboard) # клавиатура сделана в kb
            else: # Если в хранилище НЕТ этой вещи
                keyboard_loc = kb.create_in_kb(1, **{'ok': 'backpack'})
                await clb.message.edit_caption(caption=
                                                f"У вас в хранилище нет {All_Th[clb_name]}\n",
                                                reply_markup=keyboard_loc)


        # Если эта вещь лежит в Хранилище Wardrobe или Gun
        elif clb_name in list_storage_wardrobe or clb_name in list_storage_gun:
            # rez = a + b if a < b else a - b.
            if clb_name in list_storage_wardrobe:
                data_storage=(await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name]
            elif clb_name in list_storage_gun:
                data_storage=(await rq.get_StorageGun(tg_id=tg_id))[clb_name]

            logging.info(f"ВРЕМЕННО 260 --- data_storage = {data_storage} {type(data_storage)}")
            if data_storage and data_storage!='0':
                keyboard_loc = kb.create_in_kb(1, **{'ok': 'backpack'})
                await clb.message.edit_caption(caption=
                                                f"У вас в хранилище есть {All_Th[clb_name]}\n"
                                                f"Но доложить {All_Th[clb_name]} в {LBut[clb_pocket_cell.upper()]} вы не можете\n",
                                                reply_markup=keyboard_loc)

            else: # Если в хранилище НЕТ этой вещи
                keyboard_loc = kb.create_in_kb(1, **{'ok': 'backpack'})
                await clb.message.edit_caption(caption=
                                                f"У вас в хранилище нет {All_Th[clb_name]}\n",
                                                reply_markup=keyboard_loc)

# ПЕРЕЛОЖИТЬ
    elif clb_action=='perelogit':
        logging.info(f"b3! --- if clb_action == 'perelogit':")
        # создается два списка (для карманов и ячеек рюкзака) для цветных кнопок
        list_for_kb = await hf.create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell(
            tg_id=tg_id,
            value_pocket_cell=int(clb_value),
            clb_pocket_cell=clb_pocket_cell,
            backpack=clb_backpack,
            clb_name=clb_name,
            prefix='b4p'
        )
        logging.info(f"ВРЕМЕННО 361 --- list_pocket = {list_for_kb} --- list_cell = {list_for_kb} --- len(list_for_kb) = {len(list_for_kb)}")
        # создаются цветные кнопки
        if clb_backpack in [Backpack.backpack_foliage, Backpack.backpack_leana]:
            keyboard = kb.create_keyboard_from_colored_cell(
                list_pocket=list_for_kb[0],
                list_cell=list_for_kb[1],
                clb_back='backpack')
        else:
            keyboard = kb.create_keyboard_from_colored_cell(
                list_pocket=list_for_kb,
                clb_back='backpack')
        pp = '%' if clb_name in LSWG else 'шт.'
        await clb.message.edit_caption(caption=
                                                f"В какую ячейку Переложить \n{All_Th[clb_name]} {clb_value} {pp}\n",
                                                reply_markup=keyboard)



# ИСПОЛЬЗОВАТЬ
    elif clb_action=='use':
        logging.info(f"b3! --- if clb_action == 'use':")
        data_ = await rq.get_user_dict(tg_id=tg_id)
        # f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}"
        dict_kb = {'Использовать': f'b4!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{clb_value}', 'Назад': 'backpack',} # f'use1!{clb_name} там другой колбэк в "Ок"

        if clb_name in dict_u:
            keyboard = kb.create_in_kb(1, **dict_kb)
            await clb.message.edit_caption(caption=f"Вы хотите использовать {LST[clb_name.capitalize()]} \n"
                                            f"{LST[clb_name]} восстановит до {dict_u[clb_name]}ХП \n"
                                            f"У вас {data_['xp']}ХП, максимально 100ХП", reply_markup=keyboard)
        else:
            keyboard = kb.create_in_kb(1, **{'ok': 'backpack'})
            await clb.message.edit_caption(caption=f"Только лекарство можно обменять на ХП.\n"
                                            f"{All_Th[clb_name]} не лекарство",
                                            reply_markup=keyboard)
        await clb.answer()

# ВЫКИНУТЬ
    elif clb_action == 'throw_it_out':
        logging.info(f"b3! --- if clb_action == throw_it_out")
        keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(tg_id=tg_id,
                                                                             prefix='b4',
                                                                   value_pocket_cell=int(clb_value),
                                                                   value_storage=value_storage,
                                                                   clb_action=clb_action,
                                                                   clb_backpack=clb_backpack,
                                                                   clb_pocket_cell=clb_pocket_cell,
                                                                   clb_name=clb_name,
                                                                   clb_back='backpack'
                                                                   )
        await clb.message.edit_caption(caption=f"У вас {All_Th[clb_name]} {clb_value}шт.\nСколько выкинуть?",
                                       reply_markup=keyboard) # клавиатура сделана в kb

    await clb.answer()



# ДЕЙСТВИЯ на ДЕЙСТВИЯ (Положить в хранилище, Доложить, Переложить, Использовать, Выкинуть)
#
@router.callback_query(F.data.startswith('b4'))
async def b4_action(clb: CallbackQuery):
    logging.info(f"b4_action! --- clb.data = {clb.data} --- len(clb.data) = {len(clb.data)}")
    tg_id = clb.message.chat.id

    if clb.data.startswith('b4!'): # для действий 1.Положить в хранилище, 2.Доложить
        clb_button_value = clb.data.split('!')[-6] # нажатя кнопка с числом / все / до полного
        clb_action = clb.data.split('!')[-5] # действие
        clb_backpack = clb.data.split('!')[-4] # какой рюкзак надет
        clb_pocket_cell = clb.data.split('!')[-3] # в какой карман / ячейка
        clb_name = clb.data.split('!')[-2] # название вещи
        clb_value_pocket_cell = int(clb.data.split('!')[-1]) # сколько вещей в кармане / ячейке или % для
        logging.info(f"ВРЕМЕННО 348 --- clb_button_value = {clb_button_value}")
        if clb_name in list_storage_trash:
            pp = 'шт.'
        else:
            pp = '%'

    elif clb.data.startswith('b4p'): # для действий 3.Переложить
    # b4!backpack_leana!green!cell_1!20!pocket2
        clb_action = 'perelogit'
        clb_name = clb.data.split('!')[-6]
        clb_backpack = clb.data.split('!')[-5]
        clb_color_to_pc = clb.data.split('!')[-4]
        clb_from_pc = clb.data.split('!')[-3]
        clb_value_from_pc = clb.data.split('!')[-2]
        clb_to_pc = clb.data.split('!')[-1]

# ПОЛОЖИТЬ В ХРАНИЛИЩЕ и ДОЛОЖИТЬ
    if clb_action=='put_in_storage' or clb_action=='dologit':
        #logging.info(f"b4_action! --- if clb_action == 'put_in_storage' or clb_action=='dologit'")

        new_value_storage = await hf.move_select_thing_backpack_storage(
                tg_id=tg_id,
                value_pocket_cell=int(clb_value_pocket_cell),
                button_value=int(clb_button_value),
                clb_action=clb_action,
                backpack=clb_backpack,
                pocket_cell=clb_pocket_cell,
                clb_name=clb_name
        )
        if clb_button_value == '777':
            clb_button_value = 20 - clb_value_pocket_cell
        elif clb_button_value == '333' and clb_action=='put_in_storage':
            clb_button_value = clb_value_pocket_cell
        elif clb_button_value == '333' and clb_action=='dologit':
            clb_button_value = new_value_storage
        elif clb_name in LSWG:
            clb_button_value = clb_value_pocket_cell

        keyboard = kb.create_in_kb(1, **{'ok': 'backpack',})
        if clb_action=='put_in_storage':
            await clb.message.edit_caption(caption=f"Вы положили в хранилище {All_Th[clb_name]} {clb_button_value} {pp}",
                                        reply_markup=keyboard)
        elif clb_action=='dologit':
            await clb.message.edit_caption(caption=f"Вы доложили из хранилища {All_Th[clb_name]} {clb_button_value} {pp}\n",
                                           reply_markup=keyboard)

# ПЕРЕЛОЖИТЬ
    # b4_action! --- clb.data = b4p!f_aid!backpack_leana!g!cell_4!11!cell_1
    # b4_action! --- clb.data = b4p!f_aid!backpack_leana!g!pocket1!8!cell_3 --- len(clb.data.split('!')) = 7
    #                               вещь          рюкзак      цвет откуда сколько там куда
    elif clb.data.startswith('b4p'):#len(clb.data.split('!'))==6:   #clb_action == 'perelogit': 6, а не 7 элементов в колбэке
        logging.info(f"clb.data.startswith('b4_perelogit'): --- clb.data = {clb.data}")
    ### b4_action! --- clb.data = b4!backpack_leana!green!cell_2!9!pocket2

        # если перекладывают в ячейку, то минус ХП: clb_to_pc == cellN
        ### уменьшать ХП надо только если перешли из кармана в ячейку
        if 'cell' in clb_to_pc and 'pocket' in clb_from_pc:

            # ПРОВЕРКА ХП РЮКЗАКА, ЕСЛИ 0, ЗАПУСК УДАЛЕНИЯ И ПЕРЕМЕЩЕНИЯ ВЕЩЕЙ
            ## 2 МЕСТО
            #if clb_pocket_cell.startswith('cell'): # если взаимодействие с РЮКЗАКОМ - 1 хп
            #logging.info(f"if clb_pocket_cell.startswith('cell'): # если взаимодействие с РЮКЗАКОМ - 1 хп {clb_pocket_cell}")
            if not await hf.check_xp_put_on_backpack_if_more_then_zero(tg_id=tg_id): # проваливаемся сюда, если ХП < 0
                # если ХП рюкзака меньше 0, то запускаю функцию  xp_backpack_is_over_remove_things_delate_backpack
                await hf.xp_backpack_is_over_remove_things_delate_backpack(clb=clb, tg_id=tg_id, backpack=clb_backpack)
                return
        await rq.decrease_xp_put_on_backpack_1(tg_id=tg_id) # уменьшаем ХП, если нажали на рюкзак и ХП > 0


        if clb_color_to_pc == 'r':
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            keyboard = kb.create_in_kb(1, **{'Назад': 'backpack',})
            await clb.message.edit_caption(caption=f"Сюда положить нельзя", reply_markup=keyboard)
        elif clb_color_to_pc in ['y', 'g']:

            # сколько лежит там, куда хочу переложить
            # функция дает список [name_thing, value_thing]
            value_to_pc = (await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(
                tg_id=tg_id,
                backpack=clb_backpack,
                pocket_cell=clb_to_pc))[1]
            # показать кнопки сколько переложить в зависимости от количества вещей в ячейках
            # ПЕРЕЛОЖИТЬ ДЛЯ КНОПКИ "2":  '[2]': 'b5!2!perelogit! !cell_4!f_aid!11'
            keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(
                clb_pocket_cell = clb_from_pc, # откуда взять
                value_pocket_cell = int(clb_value_from_pc), # сколько лежит там откуда хочу взять
                clb_backpack = clb_to_pc, # куда положить ДЛЯ ПЕРЕЛОЖИТЬ ВМЕСТО backpack
                value_to_pc = value_to_pc, # сколько лежит там, куда хочу положить
                clb_name=clb_name,
                clb_back='backpack',
                prefix='b5',
                clb_action='perelogit'
            )

            pp = '%' if clb_name in LSWG else 'шт.'
            str_to_answer = f"уже лежит {All_Th[clb_name]} {value_to_pc} {pp}" if value_to_pc != 0 else f"ничего не лежит"

            await clb.message.edit_caption(
                caption=
                f"В {LBut[clb_to_pc.capitalize()]} {str_to_answer}\n"
                f"У вас есть {All_Th[clb_name]} {clb_value_from_pc} {pp}\n"
                f"Сколько хотите положить в {LBut[clb_to_pc.upper()]}?",
                reply_markup=keyboard)


# ИСПОЛЬЗОВАТЬ
    elif clb_action == 'use':
        logging.info(f"clb.data = {clb.data}")

        value_xp = await hf.recover_xp_subtracts_drug(
            tg_id=tg_id,
            backpack=clb_backpack,
            name_drug=clb_name,
            pocket_cell=clb_pocket_cell,
            value_drug=clb_value_pocket_cell)
        keyboard = kb.create_in_kb(1, **{'Ok': 'backpack'})

        await clb.message.edit_caption(caption=f"Вы использовали {LST[clb_name.capitalize()]} 1 шт.\n"
                                        f"Осталось {clb_value_pocket_cell-1} шт. \n"
                                        f"У вас {value_xp} ХП", reply_markup=keyboard)

        await clb.answer()

# ВЫКИНУТЬ
    elif clb_action =='throw_it_out':
        logging.info('clb_action == throw_it_out')
# Пример колбэка
# b4_action! --- clb.data = b4!1!throw_it_out!backpack_leana!cell_1!helmet_wanderer!33 --- len(clb.data.split('!')) = 7

# clb_button_value = clb.data.split('!')[-6] # нажатя кнопка с числом / все / до полного
# clb_value_pocket_cell = int(clb.data.split('!')[-1]) # сколько вещей в кармане / ячейке или % для

        if clb_button_value == '333': # Если выкинуть 333 = "Все", то выкинуть количесво вещей в ячейке = clb_value_pocket_cell
            clb_button_value = clb_value_pocket_cell
            str_answer = f"все {All_Th[clb_name.capitalize()]}"
        elif clb_name in LSWG: # Если выкинуть оружие или броню, выкидываем "все проценты" = clb_value_pocket_cell
            clb_button_value = clb_value_pocket_cell
            str_answer = f"{All_Th[clb_name]} {clb_value_pocket_cell}%"
        else:
            str_answer = f"{clb_button_value} {All_Th[clb_name.capitalize()]}"


        await hf.set_value_in_pocket_cell_put_on_backpack(
            tg_id=tg_id,
            backpack=clb_backpack,
            pocket_cell=clb_pocket_cell,
            clb_name=clb_name,
            value=clb_value_pocket_cell-int(clb_button_value)
        )
        logging.info(f'clb_button_value = {clb_button_value} --- clb_value_pocket_cell = {clb_value_pocket_cell}')
        keyboard = kb.create_in_kb(1, **{LBut['ok']: 'backpack'})
        await clb.message.edit_caption(caption=f"Вы выкинули {str_answer}",
                                       reply_markup=keyboard)

        await clb.answer()




#ПЕРЕЛОЖИТЬ
# нету в колбэке откуда переложить
### НЕ ИСПРАВЛЯТЬ НИЧЕГО! ПРОВЕРЯТЬ ДАЛЬШЕ РЮКЗАК. ИСКАТЬ ОШИБКИ И НЕСОСТЫКОВКИ
### ВНИМАНИЕ, ТУТ ОШИБКА
@router.callback_query(F.data.startswith('b5!'))
async def b5_action_continue_perelogit(clb: CallbackQuery):
    logging.info(f"b5_action_continue_perelogit --- clb.data = {clb.data} --- len(clb.data.encode('utf-8')) = {len(clb.data.encode('utf-8'))}")
    tg_id = clb.message.chat.id
#ПЕРЕЛОЖИТЬ
#  b5_action_continue_perelogit --- clb.data = b5!1!perelogit! !cell_3!shoes_reinforced!77 --- len(clb.data.encode('utf-8')) = 43
#'[2]': 'b5!2!perelogit!cell_1!cell_4!f_aid!11'
### добавить уменьшение хп если клали из кармана в ячейку
    button = clb.data.split('!')[-6]
    clb_action = clb.data.split('!')[-5]
    to_pc = clb.data.split('!')[-4]
    from_pc = clb.data.split('!')[-3]
    clb_name = clb.data.split('!')[-2]
    value_pc = clb.data.split('!')[-1]

    #
    if button == '333':
        button = value_pc
    elif button == '777':
        button = 20 - int(value_pc)

    if clb_name in LSWG: # для оружия или брони
        value_from_pc = 0
        value_to_pc = value_pc
    else:
        backpack = await hf.what_backpack_put_on(tg_id=tg_id)
        list_value_backpack = await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(tg_id=tg_id,backpack=backpack, pocket_cell=to_pc)

        value_from_pc = int(value_pc)-int(button) # откуда переносим
        value_to_pc = int(button)+int(list_value_backpack[-1]) # куда переносим

        logging.info(f'list_value_backpack = {list_value_backpack} --- value_from_pc = {value_from_pc} --- value_to_pc = {value_to_pc}')

    # откуда переносим
    await rq.set_backpack_and_cell_with_chek_put_on_backpack(
        tg_id=tg_id,
        cell=from_pc,
        name_column_cell=clb_name,
        current_value_cell=value_from_pc
    )
    # куда переносим
    await rq.set_backpack_and_cell_with_chek_put_on_backpack(
        tg_id=tg_id,
        cell=to_pc,
        name_column_cell=clb_name,
        current_value_cell=value_to_pc
    )

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N6']))
    keyboard = kb.create_in_kb(1, **{'ok': 'backpack'})
    pp = '%' if clb_name in LSWG else 'шт.'
    await clb.message.edit_caption(
        caption=f'Вы переложили {All_Th[clb_name.capitalize()]} \n'
                f'{value_to_pc} {pp} \n'
                f'в {LBut[to_pc.upper()]}\n'
                f'Здесь {All_Th[clb_name]} {value_to_pc} {pp}',
        reply_markup=keyboard)
