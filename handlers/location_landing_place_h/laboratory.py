from aiogram import F, Router, Bot

from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon_ru import (LEXICON_Invite as LI, LEXICON_BUTTON as LBut,
                                LEXICON_Laboratory as LL, LEXICON_Backpack as LB,
                                LEXICON_STORAGE_TRASH as LST, LEXICON_STORAGE_WARDROBE as LSW,
                                LEXICON_ALL_THINGS as All_Th,)
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
import database.requests as rq
import database.help_function as hf

router = Router()

storage = MemoryStorage()

import logging


# lb1 -- laboratory
@router.callback_query(F.data == 'laboratory')
async def lb1(clb: CallbackQuery,  bot: Bot):
    logging.info(f'lb1 -- {clb.data}')

    dict_kb={LL['create']: 'create', LL['dispose_of']: 'dispose_of',
            LL['repair']: 'repair','Назад': 'location_landing_place',}
    keyboard = kb.create_in_kb(2, **dict_kb)

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption=LBut['laboratory'], reply_markup=keyboard)
    await clb.answer()

# lb2 -- create
@router.callback_query(F.data == 'create')
async def lb2(clb: CallbackQuery,  bot: Bot):
    logging.info(f'lb2 - create -- {clb.data}')

    dict_kb={'Лекарства': 'drug', 'Броню': 'armor',
            'Оружие': 'guns','Назад': 'laboratory',}
    keyboard = kb.create_in_kb(1, **dict_kb)

    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption=LL['lb2'], reply_markup=keyboard)
    await clb.answer()


# lb3 -- drug | guns | armor
@router.callback_query(F.data == 'drug')
@router.callback_query(F.data == 'guns')
@router.callback_query(F.data == 'armor')
async def lb3(clb: CallbackQuery,  bot: Bot):
    logging.info(f'lb3 - {clb.data}')

    if clb.data == "drug":
        dict_kb={LST['fried_meat']: 'fried_meat', LST['fried_veins']: 'fried_veins',
                LST['bandages_s']: 'bandages_s',
                LST['f_aid_s']: 'f_aid_s', 'Назад': 'create',}

    elif clb.data == "guns":
        dict_kb={All_Th['spear']: 'spear_lab_cr', 'Назад': 'create',}

    elif clb.data == "armor":
        dict_kb={LSW['helmet_wanderer']: 'lb8!helmet_wanderer', LSW['helmet_reinforced']: 'lb8!helmet_reinforced',
                LSW['dress_wanderer']: 'lb8!dress_wanderer', LSW['dress_reinforced']: 'lb8!dress_reinforced',
                LSW['shoes_wanderer']: 'lb8!shoes_wanderer', LSW['shoes_reinforced']: 'lb8!shoes_reinforced',
                LSW['backpack_foliage']: 'lb8!backpack_foliage', LSW['backpack_leana']: 'lb8!backpack_leana',
                'Назад': 'create',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption='Что вы хотите создать?', reply_markup=keyboard)
    await clb.answer()


# lb4 -- fried_meat | fried_veins | bandages_s | f_aid_s
@router.callback_query(F.data == 'fried_meat')
@router.callback_query(F.data =='fried_veins')
@router.callback_query(F.data =='bandages_s')
@router.callback_query(F.data =='f_aid_s')
async def lb4(clb: CallbackQuery):
    logging.info(f'lb4 -- {clb.data}')
    clb_name = clb.data

    dict_kb={LL['create']: f'lb_5!{clb_name}', 'Назад': 'drug',}
    keyboard = kb.create_in_kb(1, **dict_kb)

    await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
    await clb.message.edit_caption(caption=LL[clb.data], reply_markup=keyboard)
    await clb.answer()


# lb5 -- lb_5
@router.callback_query(F.data.startswith('lb_5') )
async def lb5(clb: CallbackQuery,  bot: Bot):
    logging.info(f'lb5 -- {clb.data}')
    lb4_clb = clb.data.split('!')[-1]

    tg_id = clb.message.chat.id
    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    keyboard = kb.create_in_kb(1, **{LBut['ok']: 'create'})

    if lb4_clb == 'fried_meat':
        if data_st_tr['raw_meat']>=2 and data_st_tr['seed_zlg']>=1:
            await rq.set_storage_trash(tg_id=tg_id, name_column='raw_meat', current_value=data_st_tr['raw_meat']-2)
            await rq.set_storage_trash(tg_id=tg_id, name_column='seed_zlg', current_value=data_st_tr['seed_zlg']-1)
            await rq.set_storage_trash(tg_id=tg_id, name_column='fried_meat', current_value=data_st_tr['fried_meat']+1)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[lb4_clb]))
            await clb.message.edit_caption(caption='Вы создали'+LST[lb4_clb]+" 1 шт" , reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif lb4_clb == 'fried_veins':
        if data_st_tr['veins']>=2 and data_st_tr['seed_zlg']>=1:
            await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-2)
            await rq.set_storage_trash(tg_id=tg_id, name_column='seed_zlg', current_value=data_st_tr['seed_zlg']-1)
            await rq.set_storage_trash(tg_id=tg_id, name_column='fried_veins', current_value=data_st_tr['fried_veins']+1)

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[lb4_clb]))
            await clb.message.edit_caption(caption='Вы создали'+LST[lb4_clb]+"1 шт" , reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption=LL['lb5'], reply_markup=keyboard)
            await clb.answer()

    elif lb4_clb == 'bandages_s':
        if data_st_tr['yel_fl']>=5 and data_st_tr['vine_leaves']>=4:
            await rq.set_storage_trash(tg_id=tg_id, name_column='yel_fl', current_value=data_st_tr['yel_fl']-5)
            await rq.set_storage_trash(tg_id=tg_id, name_column='vine_leaves', current_value=data_st_tr['vine_leaves']-4)
            await rq.set_storage_trash(tg_id=tg_id, name_column='bandages_s', current_value=data_st_tr['bandages_s']+1)
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[lb4_clb]))
            await clb.message.edit_caption(caption='Вы создали'+LST[lb4_clb]+"1 шт" , reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif lb4_clb == 'f_aid_s':
        if data_st_tr['bandages_s']>=3 and data_st_tr['seed_zlg']>=2:
            await rq.set_storage_trash(tg_id=tg_id, name_column='bandages_s', current_value=data_st_tr['bandages_s']-3)
            await rq.set_storage_trash(tg_id=tg_id, name_column='seed_zlg', current_value=data_st_tr['seed_zlg']-2)
            await rq.set_storage_trash(tg_id=tg_id, name_column='f_aid_s', current_value=data_st_tr['f_aid_s']+1)
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[lb4_clb]))
            await clb.message.edit_caption(caption='Вы создали'+LST[lb4_clb]+"1 шт" , reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()


# lb6 -- spear_lab_cr
@router.callback_query(F.data == 'spear_lab_cr')
async def lb6(clb: CallbackQuery):
    logging.info(f'lb6 -- {clb.data}')

    dict_kb={LL['create']: f'lb_7', 'Назад': 'create',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['spear']))
    await clb.message.edit_caption(caption=LL['spear_create'], reply_markup=keyboard)
    await clb.answer()

# lb7 -- lb_7
@router.callback_query(F.data.startswith('lb_7') )
async def lb7(clb: CallbackQuery,  bot: Bot):
    logging.info(f'lb7 -- {clb.data}')

    tg_id = clb.message.chat.id
    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    data_bio = await rq.get_StorageBIO(tg_id=tg_id)

    data_gun = await rq.get_StorageGun(tg_id=tg_id)
    keyboard = kb.create_in_kb(1, **{LBut['ok']: 'create'})

    if data_st_tr['stick']>=31 and data_st_tr['bones']>=8 and data_st_tr['veins']>=9 and data_bio['bio'] >=150:
        await rq.set_storage_trash(tg_id=tg_id, name_column='stick', current_value=data_st_tr['stick']-31)
        await rq.set_storage_trash(tg_id=tg_id, name_column='bones', current_value=data_st_tr['bones']-8)
        await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-9)
        await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=data_bio['bio']-150)
        await rq.set_storage_gun(tg_id=tg_id, name_column='spear', current_value=f"{data_gun['spear']}!100")
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['spear']))
        await clb.message.edit_caption(caption='Вы создали Заточенное копье 1 шт.', reply_markup=keyboard)
        await clb.answer()
    else:
        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
        await clb.answer()


# lb8 -- lb_8
@router.callback_query(F.data.startswith('lb8') )
async def lb8(clb: CallbackQuery,  bot: Bot):
    data_wardrobe = await rq.get_StorageWardrobe(tg_id= clb.message.chat.id)
    #a = data_wardrobe['helmet_wanderer']
    #b = await hf.modify_str_to_dict(a)
    #c = await hf.modify_dict_to_int_with_count_thinks_value(b)
    #logging.info(f"lb8 -- {clb.data} !!! data_wardrobe['helmet_wanderer'] = {a} !!! modify_str_to_dict = {b} !!! modify_dict_to_int_with_count_thinks_value = {c}")
   # await clb.message.answer_photo(photo=ph['N40'])
    clb_data_end = clb.data.split('!')[-1]
    dict_kb={'Создать': f'lb_9!{clb_data_end}', 'Назад': 'armor',}
    keyboard = kb.create_in_kb(1, **dict_kb)
    await clb.message.edit_media(media=InputMediaPhoto(media=ph['N40']))
    await clb.message.edit_caption(caption=LL[clb_data_end], reply_markup=keyboard)
    await clb.answer()

# GOTO не понял При создании улучшенной брони ее состояние равно состоянию брони донора
# (если Шлем странника 5% то Улучшенный шлем при создании будет тоже 5%)
# lb9 -- create armor сздать броню
@router.callback_query(F.data.startswith('lb_9') )
async def lb9(clb: CallbackQuery,  bot: Bot):
    clb_name = clb.data.split('!')[-1]
    logging.info(f'lb9 -- create armor -- {clb.data} --- clb_name = {clb_name}')

    #await clb.message.answer_photo(photo=ph['N40'])
    tg_id = clb.message.chat.id
    data_st_tr = await rq.get_StorageTrash(tg_id=tg_id)
    data_bio = await rq.get_StorageBIO(tg_id=tg_id)

    data_wardrobe = await rq.get_StorageWardrobe(tg_id=tg_id)
    #helmet_wanderer = await hf.modify_str_to_dict(data_wardrobe['helmet_wanderer'])

    keyboard = kb.create_in_kb(1, **{'Ok': 'create'})


    if clb_name == 'helmet_wanderer':
        if data_bio['bio']>=200 and data_st_tr['yel_fl']>=35 and data_st_tr['stick']>=37 and data_st_tr['vine_leaves']>=28:
            #logging.info(f"lb9 -- create armor -- if clb_name == helmet_wanderer: if data_bio['bio']>=200 "
            #             f"and data_st_tr['yel_fl']>=35 and data_st_tr['stick']>=37 and data_st_tr['vine_leaves']>=28:")
            await rq.set_storage_trash(tg_id=tg_id, name_column='yel_fl', current_value=data_st_tr['yel_fl']-35)
            await rq.set_storage_trash(tg_id=tg_id, name_column='stick', current_value=data_st_tr['stick']-37)
            await rq.set_storage_trash(tg_id=tg_id, name_column='vine_leaves', current_value=data_st_tr['vine_leaves']-28)
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=data_bio['bio']-200)

            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='helmet_wanderer', current_value=data_wardrobe['helmet_wanderer']+'!100')

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'helmet_reinforced':
        helmet_wanderer = data_wardrobe['helmet_wanderer']#
        new_str_wan = await hf.modify_str_to_str_del_choise_percent_and_null(helmet_wanderer, 10000)#
        new_list_range_without_0 = new_str_wan.split('!')#
       # logging.info(f'new_str_wan = {new_str_wan} ---- new_list_ = {new_list_range_without_0}')
        if new_list_range_without_0 and new_list_range_without_0[0] and int(new_list_range_without_0[0])>0 and data_st_tr['bones']>=7 and data_st_tr['veins']>=5:#
            await rq.set_storage_trash(tg_id=tg_id, name_column='bones', current_value=data_st_tr['bones']-7)
            await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-5)

            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='helmet_reinforced', current_value=data_wardrobe['helmet_reinforced']+f'!{new_list_range_without_0[0]}')#
            new_str_without_choise = await hf.modify_str_to_str_del_choise_percent_and_null(new_str_wan, new_list_range_without_0[0])#
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='helmet_wanderer', current_value=new_str_without_choise)#

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'dress_wanderer':
        if data_bio['bio']>=230 and data_st_tr['yel_fl']>=37 and data_st_tr['stick']>=42 and data_st_tr['vine_leaves']>=33:
            await rq.set_storage_trash(tg_id=tg_id, name_column='yel_fl', current_value=data_st_tr['yel_fl']-37)
            await rq.set_storage_trash(tg_id=tg_id, name_column='stick', current_value=data_st_tr['stick']-42)
            await rq.set_storage_trash(tg_id=tg_id, name_column='vine_leaves', current_value=data_st_tr['vine_leaves']-33)
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=data_bio['bio']-230)
            # data_wardrobe['helmet_wanderer']+'!100'
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='dress_wanderer', current_value=data_wardrobe['dress_wanderer']+"!100")
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'dress_reinforced':
        wanderer_ = data_wardrobe['dress_wanderer']#
        new_str_wan = await hf.modify_str_to_str_del_choise_percent_and_null(wanderer_, 10000)#
        new_list_range_without_0 = new_str_wan.split('!')#

        if new_list_range_without_0 and new_list_range_without_0[0] and int(new_list_range_without_0[0])>0 and data_st_tr['bones']>=10 and data_st_tr['veins']>=8:
            await rq.set_storage_trash(tg_id=tg_id, name_column='bones', current_value=data_st_tr['bones']-10)
            await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-8)

            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='dress_reinforced', current_value=data_wardrobe['dress_reinforced']+f'!{new_list_range_without_0[0]}')#
            new_str_without_choise = await hf.modify_str_to_str_del_choise_percent_and_null(new_str_wan, new_list_range_without_0[0])#
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='dress_wanderer', current_value=new_str_without_choise)#

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'shoes_wanderer':
        if data_bio['bio']>=180 and data_st_tr['yel_fl']>=21 and data_st_tr['stick']>=28 and data_st_tr['vine_leaves']>=24:
            await rq.set_storage_trash(tg_id=tg_id, name_column='yel_fl', current_value=data_st_tr['yel_fl']-21)
            await rq.set_storage_trash(tg_id=tg_id, name_column='stick', current_value=data_st_tr['stick']-28)
            await rq.set_storage_trash(tg_id=tg_id, name_column='vine_leaves', current_value=data_st_tr['vine_leaves']-24)
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=data_bio['bio']-180)
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='shoes_wanderer', current_value=data_wardrobe['shoes_wanderer']+"!100")
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'shoes_reinforced':
        wanderer_ = data_wardrobe['shoes_wanderer']#
        new_str_wan = await hf.modify_str_to_str_del_choise_percent_and_null(wanderer_, 10000)#
        new_list_range_without_0 = new_str_wan.split('!')#

        if new_list_range_without_0 and new_list_range_without_0[0] and int(new_list_range_without_0[0])>0 and data_st_tr['bones']>=6 and data_st_tr['veins']>=4:
            await rq.set_storage_trash(tg_id=tg_id, name_column='bones', current_value=data_st_tr['bones']-6)
            await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-4)

            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='shoes_reinforced', current_value=data_wardrobe['shoes_reinforced']+f'!{new_list_range_without_0[0]}')#
            new_str_without_choise = await hf.modify_str_to_str_del_choise_percent_and_null(new_str_wan, new_list_range_without_0[0])#
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='shoes_wanderer', current_value=new_str_without_choise)#

            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'backpack_foliage':
        if data_bio['bio']>=100 and data_st_tr['yel_fl']>=22 and data_st_tr['stick']>=25 and data_st_tr['vine_leaves']>=18:
            await rq.set_storage_trash(tg_id=tg_id, name_column='yel_fl', current_value=data_st_tr['yel_fl']-22)
            await rq.set_storage_trash(tg_id=tg_id, name_column='stick', current_value=data_st_tr['stick']-25)
            await rq.set_storage_trash(tg_id=tg_id, name_column='vine_leaves', current_value=data_st_tr['vine_leaves']-18)
            await rq.set_storage_bio(tg_id=tg_id, name_column='bio', current_value=data_bio['bio']-100)
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='backpack_foliage', current_value=data_wardrobe['backpack_foliage']+'!100')
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()

    elif clb_name == 'backpack_leana':
        wanderer_ = data_wardrobe['backpack_foliage']#
        new_str_wan = await hf.modify_str_to_str_del_choise_percent_and_null(wanderer_, 10000)#
        new_list_range_without_0 = new_str_wan.split('!')#





        if new_list_range_without_0 and new_list_range_without_0[0] and int(new_list_range_without_0[0])>0 and data_st_tr['bones']>=3 and data_st_tr['veins']>=2:
            await rq.set_storage_trash(tg_id=tg_id, name_column='bones', current_value=data_st_tr['bones']-3)
            await rq.set_storage_trash(tg_id=tg_id, name_column='veins', current_value=data_st_tr['veins']-2)
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='backpack_leana', current_value=data_wardrobe['backpack_leana']+f'!{new_list_range_without_0[0]}')#
            new_str_without_choise = await hf.modify_str_to_str_del_choise_percent_and_null(new_str_wan, new_list_range_without_0[0])#
            await rq.set_storage_wardrobe(tg_id=tg_id, name_column='backpack_foliage', current_value=new_str_without_choise)#
            await clb.message.edit_media(media=InputMediaPhoto(media=ph[clb_name]))
            await clb.message.edit_caption(caption='Вы создали '+LST[clb_name]+" 1 шт", reply_markup=keyboard)
            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption='Не хватает ингридиентов в хранилище', reply_markup=keyboard)
            await clb.answer()