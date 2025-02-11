from aiogram import F, Router, Bot

from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_use_storage_trash as dict_u,
                                list_storage_trash_craft as craft)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf

class FSMaddNumberButton(StatesGroup):
    state_press_button = State()

router = Router()

import logging

# bio1 - F.data == ('storage_bio')
@router.callback_query(F.data == 'storage_bio')
async def bio1(clb: CallbackQuery):
    logging.info(f'bio1 -- callback_data = {clb.data}')

    tg_id = clb.message.chat.id

    data_=await rq.get_StorageBIO(tg_id=tg_id)
    value_bio = data_['bio']

    dict_kb = {LBut['bio']: 'scrp1!bio!bio', f"{value_bio}": f"bio1!{value_bio}", LBut['back']: f'storage',}
    keyboard = kb.create_in_kb(2, **dict_kb)

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N41']))
    await clb.message.edit_caption(caption=LL['bio1'], reply_markup=keyboard)
    await clb.answer()

# bio2 - F.data.startswith ('bio!')
@router.callback_query(F.data.startswith ('bio1!'))
async def bio2(clb: CallbackQuery):
    logging.info(f'bio2 - F.data.startswith (bio!) = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N41'])
    tg_id = clb.message.chat.id
    data_user = await rq.get_user_dict(tg_id=tg_id)
    if '!' in data_user['backpack']:
        backpack = data_user['backpack'].split('!')[0]
    else:
        backpack = data_user['backpack']
    value_bio = clb.data.split("!")[-1]
    if backpack != 'no_backpack':
        if int(value_bio) > 0:
            dict_kb = {LBut['take_with_u']: f"bio2!bio!{value_bio}",  LBut['back']: f'storage_bio',}
            keyboard = kb.create_in_kb(1, **dict_kb)
            #await clb.message.answer(text=LL['bio2'], reply_markup=keyboard)
            await clb.message.edit_caption(caption=LL['bio2'], reply_markup=keyboard)
            await clb.answer()
        else:
            dict_kb = {LBut['back']: f'storage_bio',}
            keyboard = kb.create_in_kb(1, **dict_kb)
            await clb.message.edit_caption(caption=LL['bio2_1'], reply_markup=keyboard)
            await clb.answer()
    else:
        dict_kb = {LBut['back']: f'storage_bio',}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_caption(caption=LL['bio2_2'], reply_markup=keyboard)
        await clb.answer()

# bio3 - F.data.startswith ('bio2!')
@router.callback_query(F.data.startswith ('bio2!'))
async def bio3(clb: CallbackQuery, state: FSMContext):
    logging.info(f'bio3 - F.data.startswith (bio1!) = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N41'])
    await state.set_state(FSMaddNumberButton.state_press_button)
    tg_id = clb.message.chat.id
    value_bio = clb.data.split('!')[-1]
    clb_name = clb.data.split('!')[-2]

    keyboard = kb.create_kb_from_1_to_9_with_all(prefix1='bio3', clb_back='storage_bio', clb_name=clb_name)
    await clb.message.edit_caption(caption=f"{LL['bio3']} {value_bio}{LL['bio3_1']}", reply_markup=keyboard)
    await clb.answer()


@router.callback_query(FSMaddNumberButton.state_press_button, F.data.startswith('bio3'))
async def bio4(clb: CallbackQuery, state: FSMContext):
    logging.info(f'bio4 - F.data.startswith (bio3!) = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N25'])
    tg_id = clb.message.chat.id
    data_bio = await rq.get_StorageBIO(tg_id=tg_id)
    bio = data_bio['bio']
    data_user = await rq.get_user_dict(tg_id=tg_id)
    if '!' in data_user['backpack']:
        backpack = data_user['backpack'].split('!')[0]
    else:
        backpack = data_user['backpack']
    clb_name = clb.data.split('!')[-2] # здесь однозначно bio
    clb_value = clb.data.split('!')[-1]
    value_backpack_bio: int = 0
    if clb_value == 'all': # Если решили положить "Все" биоресурс

        if backpack == 'backpack_foliage': # если надет лиственный рюкзак
            data_ = await rq.get_BackpackFoliage(tg_id=tg_id)
            value_backpack_bio= data_['bio']
            await rq.set_backpack_foliage(tg_id=tg_id, name_column='bio', current_value=value_backpack_bio+bio) # в рюкзаке всё био из хралилища + то, что было в рюкзаке
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=0) # в хранилище не осталось ничего: био = 0
        elif backpack == 'backpack_leana': # если надет леанный рюкзак
            data_ = await rq.get_BackpackLeana(tg_id=tg_id)
            value_backpack_bio= data_['bio']
            await rq.set_backpack_leana(tg_id=tg_id, name_column='bio', current_value=value_backpack_bio+bio) # в рюкзаке всё био из хралилища + то, что было в рюкзаке
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=0) # в хранилище не осталось ничего: био = 0

        dict_kb = {LBut['ok']: 'storage',}
        keyboard = kb.create_in_kb(1, **dict_kb)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N25']))
        await clb.message.edit_caption(caption='Вы взяли весь биоресурс', reply_markup=keyboard)
        await clb.answer()

    elif clb_value.isdigit():
        await state.update_data(button = clb_value)
        keyboard = kb.create_kb_from_1_to_0_with_ok(prefix1='bio4', clb_back='storage_bio', clb_name='bio')
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N25']))
        await clb.message.edit_caption(caption=f"{LL['bio3']} {bio}{LL['bio3_2']} {clb_value} шт.", reply_markup=keyboard)
        await clb.answer()


# продолжает нажимать на цифры пока не нажмет ОК
@router.callback_query(FSMaddNumberButton.state_press_button, F.data.startswith('bio4'))
async def bio5(clb: CallbackQuery, state: FSMContext):
    logging.info(f'bio5 - F.data.startswith (bio4!) = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N25'])
    tg_id = clb.message.chat.id
    data_bio = await rq.get_StorageBIO(tg_id=tg_id)
    value_ = data_bio['bio']
    clb_value = clb.data.split('!')[-1]
    data_press_button = await state.get_data()
    # в state добавляется в строку последнее нажатое число, пока не нажмут OK
    await state.update_data(button = data_press_button["button"]+clb_value)
    data_press_button = await state.get_data() #словарь с ключем "button"
    keyboard = kb.create_kb_from_1_to_0_with_ok(prefix1='bio4', clb_back='storage_bio', clb_name='bio')
    await clb.message.edit_caption(caption=f"{LL['bio3']} {value_}{LL['bio3_2']} {data_press_button['button']} шт.", reply_markup=keyboard)
    await clb.answer()

# закончил нажимать на цифры, нажал на ОК
@router.callback_query(FSMaddNumberButton.state_press_button, F.data.startswith('ok')) # нажили ОК
async def bio_ok(clb: CallbackQuery, state: FSMContext):
    logging.info(f"bio_ok - FSMaddNumberButton.state_press_button, F.data == 'ok' --- clb.data = {clb.data}")
    #await clb.message.answer_photo(photo=ph['N25'])
    tg_id = clb.message.chat.id
    data_state = await state.get_data()
    value_bio_button = int(data_state['button']) # сколько всего био натыкал на кнопках пользователь
    logging.info(f"bio_ok --- FSMaddNumberButton.state_press_button, F.data == 'ok' --- clb.data {clb.data} --- data_state['button']={value_bio_button}")
    data_bio = await rq.get_StorageBIO(tg_id=tg_id)
    value_bio_storage = data_bio['bio']
    bio_backpack = await hf.bio_in_what_backpack_put_on(tg_id=tg_id) # list[какой рюкзак, сколько в нем био]
    if value_bio_storage>=value_bio_button: # если биоресурса в хранилище больше, чем выбрал пользователь
        # Из хранилища вычитается
        await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=value_bio_storage-value_bio_button)
        logging.info(f"bio_ok --- value_bio_storage+value_bio_button = {value_bio_storage-value_bio_button}")
        # в рюкзак добавляется
        #logging.info(f"bio_ok --- bio_backpack[0] = {bio_backpack[0]} --- bio_backpack[1] = {bio_backpack[1]} ---  value_bio_button = {value_bio_button} --- bio_backpack[1]+value_bio_button = {bio_backpack[1]+value_bio_button}")
        await rq.set_backpack_and_cell_with_chek_put_on_backpack(tg_id=tg_id, name_column_backpack='bio', current_value_backpack=bio_backpack[1]+value_bio_button)

        keyboard = kb.create_in_kb(1, **{LBut['ok']: 'storage'})
        await clb.message.edit_caption(caption=f"Вы положили {value_bio_button} биоресурса в {LSW[bio_backpack[0]]} ", reply_markup=keyboard)
        await clb.answer()
    else: # если биоресурса в хранилище МЕНЬШЕ, чем выбрал пользователь
        keyboard = kb.create_in_kb(1, **{LBut['back']: f"bio2!bio!{value_bio_storage}"})
        await clb.message.edit_caption(caption=f"У вас нет  {value_bio_button} биоресурса ", reply_markup=keyboard)
        await clb.answer()
