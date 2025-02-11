from aiogram import F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_use_storage_trash as dict_u,
                                list_storage_trash_craft as craft, LEXICON_ALL_THINGS as All_Th)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq



router = Router()

import logging

class FSMaddNumberButtonTrash(StatesGroup):
    state_press_button_trash = State()

# use1 - startswith('tr2!use!')
@router.callback_query(F.data.startswith('tr2!use!'))
async def use1(clb: CallbackQuery):
    logging.info(f'use1 -- callback_data = {clb.data}')
    # clb.message.answer_photo(photo=ph['N25'])
    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]

    data_ = await rq.get_user_dict(tg_id=tg_id)

    dict_kb = {'Использовать': f'use1!{clb_name}', LBut['back']: f'tr1!{clb_name}!{0}',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=f"Вы хотите использовать {LST[clb_name.capitalize()]} \n"
                                    f"Она восстановит до {dict_u[clb_name]}ХП \n"
                                    f"У вас {data_['xp']}ХП, максимально 100ХП", reply_markup=keyboard)
    await clb.answer()


# use2 - startswith('use1!')
@router.callback_query(F.data.startswith('use1'))
async def use2(clb: CallbackQuery):
    logging.info(f'use2 -- callback_data = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N25'])
    tg_id = clb.message.chat.id

    clb_name = clb.data.split('!')[-1]

    value_drag_in_st_trash = (await rq.get_StorageTrash(tg_id=tg_id))[clb_name]

    value_xp = (await rq.get_user_dict(tg_id=tg_id))['xp']


    if value_xp < 100 - int(dict_u[clb_name]):
        value_xp+=int(dict_u[clb_name])
    else:
        value_xp = 100

    await rq.set_user_xp(tg_id=tg_id, current_xp=value_xp)
    await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=value_drag_in_st_trash-1)


    keyboard = kb.create_in_kb(1, **{LBut['ok']: 'storage_trash'})
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=f"Вы использовали {LST[clb_name.capitalize()]} 1 шт.\n"
                                    f"Осталось {value_drag_in_st_trash-1} шт. \n"
                                    f"У вас {value_xp} ХП", reply_markup=keyboard)
    await clb.answer()


# thr1 - startswith('tr2!throw_it_away')
@router.callback_query(F.data.startswith('tr2!throw_it_away'))
async def thr1(clb: CallbackQuery, state: FSMContext):
    logging.info(f'thr1 -- callback_data = {clb.data}')

    # состояние ожидания нажатия кнопки 1-9-ВСЕ на инлайн клавиатуре
    await state.set_state(FSMaddNumberButtonTrash.state_press_button_trash)

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1] #что надо выкинуть
    clb_value = clb.data.split('!')[-2] #сколько есть в хранилище
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    keyboard = kb.create_kb_from_1_to_9_with_all(prefix1='thr1', clb_back=f"tr1!{clb_name}!{clb_value}", clb_name=clb_name) #tr1
    await clb.message.edit_caption(caption=f"У вас {LST[clb_name]} {clb_value} шт.\n Сколько выкинуть?", reply_markup=keyboard)
    await clb.answer()


# thr2 - FSMaddNumberButton.state_press_button, F.data.startswith (thr1!)
@router.callback_query(FSMaddNumberButtonTrash.state_press_button_trash, F.data.startswith('thr1'))
async def thr2(clb: CallbackQuery, state: FSMContext):
    logging.info(f'thr2 --- FSMaddNumberButton.state_press_button, F.data.startswith (thr1!) --- clb.data = {clb.data}')

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-2]
    clb_button = clb.data.split('!')[-1]

    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    value_st_tr = data_st_tr[clb_name]
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    if clb_button == 'all':
        await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=0)
        keyboard = kb.create_in_kb(1, **{LBut['ok']: 'storage_trash'})
        await clb.message.edit_caption(caption=f"Вы выкинули все {All_Th[clb_name.capitalize()]}", reply_markup=keyboard)
        await clb.answer()
    elif clb_button.isdigit():
        await state.update_data(button = clb_button)
        keyboard = kb.create_kb_from_1_to_0_with_ok(prefix1='thr2', clb_back='storage_trash', clb_name=clb_name)
        await clb.message.edit_caption(caption=f"У вас {LST[clb_name]} {value_st_tr} шт.\n Вы собираетесь выкинуть {clb_button} шт.", reply_markup=keyboard)
        await clb.answer()

# продолжает нажимать на цифры пока не нажмет ОК
@router.callback_query(FSMaddNumberButtonTrash.state_press_button_trash, F.data.startswith('thr2'))
async def thr3(clb: CallbackQuery, state: FSMContext):
    logging.info(f'thr3 - F.data.startswith (thr2!) = {clb.data}')

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-2]
    clb_button = clb.data.split('!')[-1]
    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    value_st_tr = data_st_tr[clb_name]

    data_press_button = await state.get_data()#словарь с ключем "button"
    # в state добавляется в строку последнее нажатое число, пока не нажмут OK
    await state.update_data(button = data_press_button["button"]+clb_button)
    data_press_button = await state.get_data() #словарь с ключем "button" переопределяем для вывода на экран "Вы собираетесь взять..."
    keyboard = kb.create_kb_from_1_to_0_with_ok(prefix1='thr2', clb_back='storage_trash', clb_name=clb_name) # здесь prefix1 такой же как и на входе в эту функцию
    await clb.message.edit_caption(caption=f"У вас {LST[clb_name]} {value_st_tr} шт.\n Вы собираетесь выкинуть {data_press_button['button']} шт.", reply_markup=keyboard)
    await clb.answer()


# закончил нажимать на цифры, нажал на ОК
@router.callback_query(FSMaddNumberButtonTrash.state_press_button_trash, F.data.startswith('ok')) # нажили ОК clb.data = ok.clb_name
async def thr_ok(clb: CallbackQuery, state: FSMContext):
    logging.info(f"thr_ok - FSMaddNumberButtonTrash.state_press_button_trash, F.data == 'ok' --- clb.data = {clb.data}")

    tg_id = clb.message.chat.id
    clb_name = clb.data.split('!')[-1]

    data_state = await state.get_data()
    value_trash_button = int(data_state['button']) # сколько всего био натыкал на кнопках пользователь
    logging.info(f"thr_ok - FSMaddNumberButtonTrash.state_press_button_trash, F.data == 'ok' --- clb.data = {clb.data} --- data_state['button']={value_trash_button}")
    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    value_st_tr = data_st_tr[clb_name]

    if value_st_tr>=value_trash_button: # если биоресурса в хранилище больше, чем выбрал пользователь
        # Из хранилища выбрасывается
        await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=value_st_tr-value_trash_button)

        keyboard = kb.create_in_kb(1, **{LBut['ok']: 'storage'})
        await clb.message.edit_caption(caption=f"Вы выкинули {value_trash_button} {LST[clb_name]}", reply_markup=keyboard)
        await clb.answer()
    else: # если биоресурса в хранилище МЕНЬШЕ, чем выбрал пользователь
        keyboard = kb.create_in_kb(1, **{LBut['back']: f"thr1!{clb_name}!{value_st_tr}"})
        await clb.message.edit_caption(caption=f"У вас нет  {value_trash_button} {All_Th[clb_name]} ", reply_markup=keyboard)
        await clb.answer()
    state.clear()