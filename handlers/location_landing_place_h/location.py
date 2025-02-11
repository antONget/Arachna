from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut, LEXICON_Laboratory as LL,
                                LEXICON_scribe_trash as LScrTr, LEXICON_scribe_wardrobe as LScrWard,
                                LEXICON_scribe_gun as LScrGun, dict_repair_description)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq

router = Router()

import logging


# lp1 - location_landing_place
@router.callback_query(F.data == 'location_landing_place')
async def lp1(clb: CallbackQuery):
    logging.info(f'location_landing_place')
    #await clb.message.answer_photo(photo=ph['N5'])
    dict_kb={LBut['storage']: 'storage', LBut['laboratory']: 'laboratory',
            LBut['back']: 'start',}
    keyboard = kb.create_in_kb(2, **dict_kb)
    #await clb.message.answer(text=LI['landing_place'], reply_markup=keyboard)

    #await clb.message.answer_photo(photo=ph['N18'],
     #                              caption=LI['landing_place'],
      #                             reply_markup=keyboard)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N5']))
    await clb.message.edit_caption(caption=LI['landing_place'], reply_markup=keyboard)
    await clb.answer()

# lp2 - storage
@router.callback_query(F.data == 'storage')
async def lp2(clb: CallbackQuery, bot: Bot):
    logging.info(f'callback_data = {clb.data}')
    #await clb.message.answer_photo(photo=ph['N18'])
    dict_kb={LBut['storage_trash']: 'storage_trash', LBut['storage_wardrobe']: 'storage_wardrobe',
            LBut['storage_guns']: 'storage_gun', LBut['storage_bio']: 'storage_bio',
            'Назад': 'location_landing_place',}
    keyboard = kb.create_in_kb(2, **dict_kb)
    #await clb.message.answer(text=LI['landing_place'], reply_markup=keyboard)

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N18']))
    await clb.message.edit_caption(caption=LI['landing_place'], reply_markup=keyboard)
    await clb.answer()

# scrp1!
@router.callback_query(F.data.startswith('scrp1'))
async def scrp1(clb: CallbackQuery):
    logging.info(f'scrp1! -- callback_data = {clb.data}')

    clb_part = clb.data.split('!')[1]
    clb_name = clb.data.split('!')[2]

    if clb_part.startswith('tr1'):
        #await clb.message.answer_photo(photo=ph['N24'])
        keyboard = kb.create_in_kb(1, **{LBut['back']: 'storage_trash'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=LScrTr[clb_name], reply_markup=keyboard)

    elif clb_part.startswith('bio'):
        #await clb.message.answer_photo(photo=ph['N23'])
        keyboard = kb.create_in_kb(1, **{LBut['back']: 'storage_bio'})
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N41']))# bio
        await clb.message.edit_caption(caption=LScrTr[clb_name], reply_markup=keyboard)

    elif clb_part.startswith('ward1'):
        #await clb.message.answer_photo(photo=ph['N24'])
        keyboard = kb.create_in_kb(1, **{LBut['back']: 'storage_wardrobe'})
       # await clb.message.answer(text=LScrWard[clb_name], reply_markup=keyboard)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=LI['landing_place'], reply_markup=keyboard)

    elif clb_part.startswith('ward_not_landing_place'):
       # await clb.message.answer_photo(photo=ph['N24'])
        keyboard = kb.create_in_kb(1, **{LBut['back']: 'function_what_remaind_things'})
        #await clb.message.answer(text=LScrWard[clb_name], reply_markup=keyboard)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=LScrWard[clb_name], reply_markup=keyboard)

    elif clb_part.startswith('st_gun'):
       # await clb.message.answer_photo(photo=ph['N24'])
        keyboard = kb.create_in_kb(1, **{LBut['back']: 'storage_gun'})
       # await clb.message.answer(text=LScrGun[clb_name], reply_markup=keyboard)
        await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
        await clb.message.edit_caption(caption=LScrGun[clb_name], reply_markup=keyboard)
   # elif clb_part.startswith('st_gun'):
    #    await clb.message.answer_photo(photo=ph['N24'])
     #   keyboard = kb.create_in_kb(1, **{LBut['back']: 'storage_gun'})
      #  await clb.message.answer(text=LScrGun[clb_name], reply_markup=keyboard)
