from aiogram import F, Router, Bot

from aiogram.types import CallbackQuery, InputMediaPhoto

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_storage_trash_bio,
                                list_storage_trash_craft as craft, LEXICON_ALL_THINGS as All_Th)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf


router = Router()

import logging

# tr1 - storage_trash
@router.callback_query(F.data == 'storage_trash')
async def storage_trash(clb: CallbackQuery):
    logging.info(f'storage_trash -- callback_data = {clb.data}')

    tg_id = clb.message.chat.id

    dict_: dict = await rq.get_StorageTrash(tg_id=tg_id)
    dict_st_tr = await hf.modify_dict_to_without_null(dict_)
    logging.info(f'storage_trash -- dict_st_tr = {dict_st_tr}')

    # проверям условие, что в хранилище что-то есть
    if not dict_st_tr: # если словарь пустой
        logging.info(f'not dict_st_tr.keys:')

        dict_kb = {LBut['back']: 'storage'}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N19']))
        await clb.message.edit_caption(caption='У вас ничего нет', reply_markup=keyboard)
        await clb.answer()
    else: # если словарь НЕ пустой
        logging.info(f'Словарь не пустой:')

        logging.info(f'Словарь не пустой: после фото')
        keyboard = kb.create_list_in_kb(width=2, dict_= dict_st_tr, prefix1= 'scrp1!tr1',
                                        prefix2='tr1', clb_back_str='storage')
        logging.info(f'Словарь не пустой: после фото после кейборда')
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N19']))
        await clb.message.edit_caption(caption='В хранилище находится:', reply_markup = keyboard)
        await clb.answer()


# tr2 - startswith('tr1!')   '1 шт.': 'tr1!canned_meat!1',
@router.callback_query(F.data.startswith('tr1!'))
async def tr1(clb: CallbackQuery):
    logging.info(f'tr1 -- callback_data = {clb.data}')

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]


    dict_st_tr: dict = await rq.get_StorageTrash(tg_id=tg_id)
    value = dict_st_tr[clb_name]

    if clb_name in craft: # для лекарства и крафта разная клава, крафт нельзя "Использовать"
        dict_kb = {'Положить в рюкзак': f'tr2!put_in_backpack!{clb_name}!{clb_value}', ### ой, почему не передается количество трэша?
                    LBut['throw_it_away']: f'tr2!throw_it_away!{value}!{clb_name}',
                    LBut['back']: 'storage_trash',}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"{LST[clb_name]} {str(value)} шт.\n"
                                       f"{LL['tr2']}", reply_markup=keyboard)
        await clb.answer()

    else: # Лекарство можно "Использовать"
        dict_kb = {LBut['put_in_backpack']: f'tr2!put_in_backpack!{clb_name}!{clb_value}',
                    LBut['use']: f'tr2!use!{clb_name}',
                    LBut['throw_it_away']: f'tr2!throw_it_away!{value}!{clb_name}',
                    LBut['back']: 'storage_trash',}

        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=f"{LST[clb_name]} {str(value)} шт.\n"
                                    f"{LL['tr2']}", reply_markup=keyboard)
        await clb.answer()


# tr2 - startswith('tr2!put_in_backpack')
@router.callback_query(F.data.startswith('tr2!put_in_backpack'))
async def tr2(clb: CallbackQuery):
    logging.info(f'tr2 -- callback_data = {clb.data}')

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-2]
    clb_value = clb.data.split('!')[-1]
    backpack = await hf.what_backpack_put_on(tg_id)

    list_for_kb = await hf.create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell(
            tg_id=tg_id,
            value_pocket_cell=int(clb_value),
            #clb_pocket_cell=clb_pocket_cell,
            backpack=backpack,
            clb_name=clb_name,
            prefix='tr3!'
        )
    logging.info(f"ВРЕМЕННО 361 --- list_pocket = {list_for_kb[0]} --- list_cell = {list_for_kb[1]} --- len(list_for_kb) = {len(list_for_kb)}")
    # создаются цветные кнопки
    if backpack in ['backpack_foliage', 'backpack_leana']:
        keyboard = kb.create_keyboard_from_colored_cell(
            list_pocket=list_for_kb[0],
            list_cell=list_for_kb[1],
            clb_back=f'tr1!{clb_name}!{clb_value}')
    else:
        keyboard = kb.create_keyboard_from_colored_cell(
            list_pocket=list_for_kb,
            clb_back=f'tr1!{clb_name}!{clb_value}')

    await clb.message.edit_caption(caption=
                                            f"В какую ячейку кладем \n{All_Th[clb_name]} {clb_value} шт.\n",
                                            reply_markup=keyboard)




# tr3 - startswith('tr3!')
@router.callback_query(F.data.startswith('tr3!'))
async def tr3(clb: CallbackQuery):
    logging.info(f'tr3 -- callback_data = {clb.data}') # tr4 -- callback_data = tr3!!f_aid!backpack_leana!g!X!3!cell_3

    tg_id = clb.message.chat.id

    clb_name = clb.data.split('!')[-6]
    clb_backpack = clb.data.split('!')[-5]
    clb_color_to_pc = clb.data.split('!')[-4]
    #clb_from_pc = clb.data.split('!')[-3]
    value_storage = clb.data.split('!')[-2] # cколько лежит в хранилище, сколько хочу положить
    clb_to_pc = clb.data.split('!')[-1]

    if 'cell' in clb_to_pc: # если перекладывают в ячейку, то минус ХП: clb_to_pc == cellN
            await rq.decrease_xp_put_on_backpack_1(tg_id)
    if clb_color_to_pc == 'r':
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        keyboard = kb.create_in_kb(1, **{'Назад': 'storage_trash',})
        await clb.message.edit_caption(caption=f"Сюда положить нельзя", reply_markup=keyboard)
    elif clb_color_to_pc in ['y', 'g']:

        # сколько лежит там, куда хочу переложить
        # функция дает список [name_thing, value_thing]
        value_to_pc = (await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(
            tg_id=tg_id,
            backpack=clb_backpack,
            pocket_cell=clb_to_pc))[1]

        keyboard = await kb.create_kb_to_remove_backpack_to_storage_and_back(
                #clb_pocket_cell = clb_from_pc, # откуда взять
                value_storage = int(value_storage), # cколько лежит в хранилище, сколько хочу положить
                value_pocket_cell = int(value_to_pc), # сколько лежит там откуда хочу взять

                clb_backpack = clb_backpack, # куда положить ДЛЯ ПЕРЕЛОЖИТЬ ВМЕСТО backpack
                clb_pocket_cell= clb_to_pc,
                clb_name=clb_name,
                clb_back='storage_trash',
                prefix='tr4',
                clb_action='dologit'
            )
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        if clb_color_to_pc == 'g':
            await clb.message.edit_caption(
                caption=
                f"У вас есть {All_Th[clb_name]} {value_storage} шт."
                f"Сколько хотите положить в {LBut[clb_to_pc.upper()]}?",
                reply_markup=keyboard)

        elif clb_color_to_pc == 'y':
            await clb.message.edit_caption(
                caption=
                f"В {All_Th[clb_to_pc.capitalize()]} уже лежит {All_Th[clb_name]} {value_to_pc} шт.\n"
                f"У вас есть {All_Th[clb_name]} {value_storage} шт. \n"
                f"Сколько хотите положить в {LBut[clb_to_pc.upper()]}?",
                reply_markup=keyboard)





# tr4 - startswith('tr4!')
@router.callback_query(F.data.startswith('tr4!'))
async def tr4(clb: CallbackQuery):
    logging.info(f'tr4 -- callback_data = {clb.data}') #  tr4 -- callback_data = tr4!2!dologit!backpack_leana!cell_2!f_aid!0

    tg_id = clb.message.chat.id
    clb_value_button = int(clb.data.split('!')[-6])
    clb_backpack = clb.data.split('!')[-4] # Если нажат КАРМАН, эта информация не нужна
    clb_pocket_cell = clb.data.split('!')[-3]

    clb_name = clb.data.split('!')[-2]
    value_to_pc = int(clb.data.split('!')[-1])

    value_pc = (await hf.what_thing_value_in_the_pocket_cell_put_on_backpack(tg_id, clb_pocket_cell, clb_backpack))[-1]
    value_trash = (await rq.get_StorageTrash(tg_id))[clb_name]
    if clb_value_button == 333:
        clb_value_button = value_trash
    elif clb_value_button == 777:
        clb_value_button = 20 - value_pc


    # откуда переносим (из хранилища Хлам забираем это количество вещей)

    new_value_trash = value_trash - clb_value_button
    await rq.set_storage_trash(tg_id, clb_name, new_value_trash)

    # куда переносим
    new_value_pc = value_to_pc + clb_value_button
    await hf.set_value_in_pocket_cell_put_on_backpack(
        tg_id=tg_id,
        pocket_cell=clb_pocket_cell,
        clb_name=clb_name,
        value=new_value_pc,
        backpack=clb_backpack
    )

    kb_dict = {'ok': "storage"}
    keyboard = kb.create_in_kb(1, **kb_dict)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
    await clb.message.edit_caption(caption='Вы положили '+ All_Th[clb_name.upper()]+ ' ' + str(clb_value_button) + ' шт.\nв ' +
                                  All_Th[clb_pocket_cell.upper()], reply_markup=keyboard)
    await clb.answer()
