from aiogram import F, Router, Bot

from aiogram.types import CallbackQuery, InputMediaPhoto

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                list_storage_trash as lst, dict_storage_trash_bio,)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf

router = Router()

import logging


# d1 -- laboratory
@router.callback_query(F.data == 'dispose_of')
async def d1(clb: CallbackQuery):
    logging.info(f'd1 -- {clb.data}')
    tg_id = clb.message.chat.id
    #await clb.message.answer_photo(photo=ph['N40'])
    dst = await rq.get_StorageTrash(tg_id=tg_id)

    dict_is_in_st_tr = await rq.get_StorageTrash(tg_id=tg_id)


    logging.info(f'd1 -- update_dict{dict_is_in_st_tr}')



    dict_kb = await hf.modify_dict_to_without_null(dict_is_in_st_tr)

    logging.info(f'd1 -- dict_kb = {dict_kb}')

    dict_: dict = {}
    for key in dict_kb:
        ### Структура колбэка d1! + key = name_column + number of unit

        dict_[LST[key] +" "+ dict_storage_trash_bio[key]+ " био"] = "d1!"+key +'!'+ str(dict_is_in_st_tr[key])### Колбэк тут

    logging.info(f'd1 -- dict_сb = {dict_kb}')
    dict_[LBut['back']] = 'laboratory'
    keyboard = kb.create_in_kb(1, **dict_)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption=LL['d1'], reply_markup=keyboard)
    await clb.answer()

# d2 -- "d1!"+key
@router.callback_query(F.data.startswith('d1!') )
async def d2(clb: CallbackQuery):
    logging.info(f'd2 -- {clb.data}')
    clb_all = clb.data.split('!', 1)[-1]
    clb_name = clb.data.split('!')[-2]
    clb_namber = clb.data.split('!')[-1]

    kb_dict = {'1': f'd2!1!{clb_all}', '2': f'd2!2!{clb_all}', '3': f'd2!3!{clb_all}', '4': f'd2!4!{clb_all}',
               '5': f'd2!5!{clb_all}', '6': f'd2!6!{clb_all}', '7': f'd2!7!{clb_all}', '8': f'd2!8!{clb_all}', '9': f'd2!9!{clb_all}',
               'Bce': f'd2!Bce!{clb_all}', LBut['back']: 'dispose_of'}
    keyboard = kb.create_in_kb(3, **kb_dict)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=LL['d2']+LST[clb_name]+' '+str(clb_namber)+LL['d2_1'], reply_markup=keyboard)
    await clb.answer()


# d3 -- "d2!"+key
@router.callback_query(F.data.startswith('d2!') )
async def d3(clb: CallbackQuery):
    logging.info(f'd3 -- {clb.data}')
    clb_name = clb.data.split('!')[2]
    clb_number = clb.data.split('!')[3]
    clb_button = clb.data.split('!')[1]

    tg_id = clb.message.chat.id
    data_st = await rq.get_StorageTrash(tg_id=tg_id)
    kb_dict = {LBut['ok']: 'dispose_of'}
    keyboard = kb.create_in_kb(1, **kb_dict)
    bio_value = (await rq.get_StorageBIO(tg_id))['bio']
    if clb_button == 'Bce':
            logging.info(f'd3 -- clb_button == Bce')
            await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=0)
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio',
                                    current_value=bio_value + (int(clb_number)*int(dict_storage_trash_bio[clb_name])))
            #await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption=LL['d3_1']+ clb_button +' '+ LST[clb_name]+LL['d3_2']+
                                     str(int(dict_storage_trash_bio[clb_name])*int(clb_number))+LL['d3_3'], reply_markup=keyboard)
            await clb.answer()
    else: # кнопки с числами
        if int(clb_button) > int(clb_number): # нажатая кнопка больше, чем есть в хранилище
            logging.info(f'd3 -- clb_button == НЕ валидное значение')
            await clb.message.edit_caption(caption='У вас нет '+clb_button + ' ' + LST[clb_name], reply_markup=keyboard)
            await clb.answer()
        else:
            logging.info(f'd3 -- clb_number == валидное значение. bio = {data_st}')#.bio}')
            await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=int(clb_number)-int(clb_button))
            await rq.set_storage_bio(tg_id=tg_id, name_column= 'bio',
                                    current_value = bio_value +(int(clb_button)*int(dict_storage_trash_bio[clb_name])))
            await clb.message.edit_caption(caption='Вы Утилизировали '+  clb_button+' '+LST[clb_name]+LL['d3_2']+
                                     str(int(dict_storage_trash_bio[clb_name])*int(clb_button))+LL['d3_3'], reply_markup=keyboard)
            await clb.answer()
