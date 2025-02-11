from database.models import (User, StorageTrash, StorageWardrobe, StorageGun, StorageBIO,
                             BackpackFoliage, BFoliageCell_1, BFoliageCell_2,
                             BackpackLeana, BLeanaCell_1, BLeanaCell_2, BLeanaCell_3, BLeanaCell_4,
                             Pocket1, Pocket2,

                              )
from database.models import async_session
import database.help_function as hf
#from database.help_function import Backpack, Location
from sqlalchemy import select
from dataclasses import dataclass
from aiogram.types import Message
import logging


async def add_new_user(data:dict):
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == int(data["tg_id"])))
        if not user:
            session.add(User(**data))
            session.add(StorageTrash(**data))
            session.add(StorageWardrobe(**data))
            session.add(StorageGun(**data))
            session.add(StorageBIO(**data))
            session.add(BackpackFoliage(**data))
            session.add(BFoliageCell_1(**data))
            session.add(BFoliageCell_2(**data))
            session.add(BackpackLeana(**data))
            session.add(BLeanaCell_1(**data))
            session.add(BLeanaCell_2(**data))
            session.add(BLeanaCell_3(**data))
            session.add(BLeanaCell_4(**data))
            session.add(Pocket1(**data))
            session.add(Pocket2(**data))

            await session.commit()

async def get_users() -> User:
    logging.info(f'get_users')
    async with async_session() as session:
        return await session.scalars(select(User))

async def get_user(tg_id: int) -> User:
    logging.info(f'get_user')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

async def get_user_dict(tg_id: int) -> dict:
    #logging.info(f'get_user_dict')
    async with async_session() as session:
        data: User = await session.scalar(select(User).where(User.tg_id == tg_id))

        dict_: dict = {}

        dict_['name_user']= data.name_user

        dict_['xp']= data.xp
        dict_['kristals'] = data.kristals
        dict_['location'] = data.location
        dict_['time'] = data.time

        #dict_['pocket1'] = data.pocket1
        #dict_['pocket2'] = data.pocket2

        dict_['backpack'] = data.backpack
        dict_['xp_backpack'] = data.xp_backpack

        dict_['helmet'] = data.helmet
        dict_['xp_helmet'] = data.xp_helmet
        dict_['dress'] = data.dress
        dict_['xp_dress'] = data.xp_dress
        dict_['shoes'] = data.shoes
        dict_['xp_shoes'] = data.xp_shoes
        dict_['left_hand'] = data.left_hand
        dict_['xp_left_hand'] = data.xp_left_hand
        dict_['right_hand'] = data.right_hand
        dict_['xp_right_hand'] = data.xp_right_hand
        return dict_

async def get_StorageTrash(tg_id: int) -> dict:
    logging.info(f'get_StorageTrash')
    async with async_session() as session:
        data: StorageTrash = await session.scalar(select(StorageTrash).where(StorageTrash.tg_id == tg_id))

        dict_: dict = {}

        dict_['f_aid']=data.f_aid
        dict_['f_aid_s']=data.f_aid_s
        dict_['bandages']=data.bandages
        dict_['bandages_s'] = data.bandages_s
        dict_['canned_meat'] = data.canned_meat
        dict_['fried_meat'] = data.fried_meat
        dict_['fried_veins'] = data.fried_veins
        dict_['berries'] = data.berries
        dict_['bones'] = data.bones
        dict_['veins'] = data.veins
        dict_['vine_leaves'] = data.vine_leaves
        dict_['yel_fl'] = data.yel_fl
        dict_['stick'] = data.stick
        dict_['raw_meat'] = data.raw_meat
        dict_['seed_zlg'] = data.seed_zlg

    return dict_

async def get_StorageWardrobe(tg_id: int) -> dict:
    logging.info(f'get_StorageWardrobe')
    async with async_session() as session:
        data: StorageWardrobe = await session.scalar(select(StorageWardrobe).where(StorageWardrobe.tg_id == tg_id))

        dict_: dict = {}

        dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        dict_['helmet_wanderer'] = data.helmet_wanderer
        dict_['helmet_reinforced'] = data.helmet_reinforced
        dict_['dress_kosmonavt'] = data.dress_kosmonavt
        dict_['dress_wanderer'] = data.dress_wanderer
        dict_['dress_reinforced'] = data.dress_reinforced
        dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        dict_['shoes_wanderer'] = data.shoes_wanderer
        dict_['shoes_reinforced'] = data.shoes_reinforced
        dict_['backpack_foliage'] = data.backpack_foliage
        dict_['backpack_leana'] = data.backpack_leana

        return dict_

async def get_StorageGun(tg_id: int) -> dict:
    logging.info(f'get_StorageGun')
    async with async_session() as session:
        data: StorageGun = await session.scalar(select(StorageGun).where(StorageGun.tg_id==tg_id))
        dict_: dict = {}

        dict_['G17'] = data.G17
        dict_['spear'] = data.spear
        dict_['nothink'] = data.nothink

        return dict_

async def get_StorageBIO(tg_id: int) -> dict:
    logging.info(f'get_StorageBIO')
    async with async_session() as session:
        data: StorageBIO = await session.scalar(select(StorageBIO).where(StorageBIO.tg_id ==tg_id))
        dict_: dict = {}

        dict_['bio'] = data.bio

        return dict_

async def get_BackpackFoliage(tg_id: int) -> dict:
    logging.info(f'get_BackpackFoliage')
    async with async_session() as session:
        data: BackpackFoliage = await session.scalar(select(BackpackFoliage).where(BackpackFoliage.tg_id ==tg_id))
        dict_: dict = {}

        dict_['cell_1'] = data.cell_1
        dict_['cell_2'] = data.cell_2
        dict_['clb_back'] = data.clb_back
        dict_['bio'] = data.bio

        return dict_

async def get_BFoliageCell_1(tg_id: int) -> dict:
    logging.info(f'get_BFoliageCell_1')
    async with async_session() as session:
        data: BFoliageCell_1 = await session.scalar(select(BFoliageCell_1).where(BFoliageCell_1.tg_id ==tg_id))
        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_BFoliageCell_2(tg_id: int) -> dict:
    logging.info(f'get_BFoliageCell_2')
    async with async_session() as session:
        data: BFoliageCell_2 = await session.scalar(select(BFoliageCell_2).where(BFoliageCell_2.tg_id ==tg_id))
        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_BackpackLeana(tg_id: int) -> dict:
    logging.info(f'get_BackpackLeana')
    async with async_session() as session:
        data: BackpackLeana = await session.scalar(select(BackpackLeana).where(BackpackLeana.tg_id ==tg_id))
        dict_: dict = {}

        dict_['cell_1'] = data.cell_1
        dict_['cell_2'] = data.cell_2
        dict_['cell_3'] = data.cell_3
        dict_['cell_4'] = data.cell_4

        dict_['xp'] = data.xp
        dict_['bio'] = data.bio

        return dict_

async def get_BLeanaCell_1(tg_id: int) -> dict:
    logging.info(f'get_BLeanaCell_1')
    async with async_session() as session:
        data: BLeanaCell_1 = await session.scalar(select(BLeanaCell_1).where(BLeanaCell_1.tg_id ==tg_id))

        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_BLeanaCell_2(tg_id: int) -> dict:
    logging.info(f'get_BLeanaCell_2')
    async with async_session() as session:
        data: BLeanaCell_2 = await session.scalar(select(BLeanaCell_2).where(BLeanaCell_2.tg_id ==tg_id))
        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_BLeanaCell_3(tg_id: int) -> dict:
    logging.info(f'get_BLeanaCell_3')
    async with async_session() as session:
        data: BLeanaCell_3 = await session.scalar(select(BLeanaCell_3).where(BLeanaCell_3.tg_id ==tg_id))
        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_BLeanaCell_4(tg_id: int) -> dict:
    logging.info(f'get_BLeanaCell_4')
    async with async_session() as session:
        data: BLeanaCell_4 = await session.scalar(select(BLeanaCell_4).where(BLeanaCell_4.tg_id ==tg_id))
        dict_: dict = {}

        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries

        if data.bones>0:
            dict_['bones'] = data.bones
        if data.veins>0:
            dict_['veins'] = data.veins
        if data.vine_leaves>0:
            dict_['vine_leaves'] = data.vine_leaves
        if data.yel_fl>0:
            dict_['yel_fl'] = data.yel_fl
        if data.stick>0:
            dict_['stick'] = data.stick
        if data.raw_meat>0:
            dict_['raw_meat'] = data.raw_meat
        if data.seed_zlg>0:
            dict_['seed_zlg'] = data.seed_zlg

        if data.helmet_kosmonavt>0:
            dict_['helmet_kosmonavt'] = data.helmet_kosmonavt
        if data.helmet_wanderer>0:
            dict_['helmet_wanderer'] = data.helmet_wanderer
        if data.helmet_reinforced>0:
            dict_['helmet_reinforced'] = data.helmet_reinforced
        if data.dress_kosmonavt>0:
            dict_['dress_kosmonavt'] = data.dress_kosmonavt
        if data.dress_wanderer>0:
            dict_['dress_wanderer'] = data.dress_wanderer
        if data.dress_reinforced>0:
            dict_['dress_reinforced'] = data.dress_reinforced
        if data.shoes_kosmonavt>0:
            dict_['shoes_kosmonavt'] = data.shoes_kosmonavt
        if data.shoes_wanderer>0:
            dict_['shoes_wanderer'] = data.shoes_wanderer
        if data.shoes_reinforced>0:
            dict_['shoes_reinforced'] = data.shoes_reinforced
        if data.backpack_foliage>0:
            dict_['backpack_foliage'] = data.backpack_foliage
        if data.backpack_leana>0:
            dict_['backpack_leana'] = data.backpack_leana
        if data.G17>0:
            dict_['G17'] = data.G17
        if data.spear>0:
            dict_['spear'] = data.spear
        if data.nothink>0:
            dict_['nothink'] = data.nothink

        return dict_

async def get_Pocket1(tg_id: int) -> dict:
    """словарь из из модуля Pocket1, без User"""
    logging.info(f'get_Pocket1')
    async with async_session() as session:
        data: Pocket1 = await session.scalar(select(Pocket1).where(Pocket1.tg_id ==tg_id))
        dict_: dict = {}
        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries
        return dict_

async def get_Pocket2(tg_id: int) -> dict:
    """словарь из из модуля Pocket2, без User"""
    logging.info(f'get_Pocket2')
    async with async_session() as session:
        data: Pocket2 = await session.scalar(select(Pocket2).where(Pocket2.tg_id==tg_id))
        dict_: dict = {}
        if data.f_aid>0:
            dict_['f_aid'] = data.f_aid
        if data.f_aid_s>0:
            dict_['f_aid_s'] = data.f_aid_s
        if data.bandages>0:
            dict_['bandages'] = data.bandages
        if data.bandages_s>0:
            dict_['bandages_s'] = data.bandages_s
        if data.canned_meat>0:
            dict_['canned_meat'] = data.canned_meat
        if data.fried_meat>0:
            dict_['fried_meat'] = data.fried_meat
        if data.fried_veins>0:
            dict_['fried_veins'] = data.fried_veins
        if data.berries>0:
            dict_['berries'] = data.berries
        return dict_

### Останется тут до поры, до времени
#set nickname
async def set_user_nickname(tg_id: int, new_nickname: str):
    logging.info(f'set_user_nickname')
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.name_user = new_nickname
        await session.commit()

# set общего ХП
async def set_user_xp(tg_id: int, current_xp: int):
    logging.info(f'set_user_xp')
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.xp = current_xp
        await session.commit()

# изменение хр лиственного рюкзака на -1
#async def decrease_xp_backpack_foliage_1 (tg_id: int) -> BackpackFoliage:
#    logging.info(f'decrease_xp_backpack_1')
#    async with async_session() as session:
#        backpak_xp: BackpackFoliage = await session.scalar(select(BackpackFoliage).where(BackpackFoliage.tg_id == tg_id))
#        backpak_xp.xp -= 1
#        await session.commit()

# изменение хр Леанного рюкзака на -1
#async def decrease_xp_backpack_leana_1 (tg_id: int) -> BackpackFoliage:
#    logging.info(f'decrease_xp_backpack_leana_1')
#    async with async_session() as session:
#        backpak_xp: BackpackLeana = await session.scalar(select(BackpackLeana).where(BackpackLeana.tg_id == tg_id))
#        backpak_xp.xp -= 1
#        await session.commit()

# уменьшает хр НАДЕТОГО рюкзака на -1
async def decrease_xp_put_on_backpack_1 (tg_id: int) -> BackpackFoliage:
    """ уменьшает хр НАДЕТОГО рюкзака на -1 ПЕРЕДЕЛКА для таблицы user """
    logging.info(f'decrease_xp_put_on_backpack_1')

    async with async_session() as session:
        backpak_xp: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        backpak_xp.xp_backpack -= 1
        await session.commit()


async def set_user(tg_id: int, name_column: str, current_value: int | str ) -> User:
    logging.info(f'set_user {tg_id} {name_column} {current_value}')
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        if name_column == 'xp':
            user.xp = current_value
        elif name_column == 'name_user':
            user.name_user = current_value
        elif name_column == 'kristals':
            user.kristals = current_value
        elif name_column == 'location':
            user.location = current_value
        elif name_column == 'time':
            user.time = current_value
        elif name_column == 'backpack':
            user.backpack = current_value
        elif name_column == 'xp_backpack':
            user.xp_backpack = current_value
        elif name_column == 'helmet':
            user.helmet = current_value
        elif name_column == 'xp_helmet':
            user.xp_helmet = current_value
        elif name_column == 'dress':
            user.dress = current_value
        elif name_column == 'xp_dress':
            user.xp_dress = current_value
        elif name_column == 'shoes':
            user.shoes = current_value
        elif name_column == 'xp_shoes':
            user.xp_shoes = current_value
        elif name_column == 'left_hand':
            user.left_hand = current_value
        elif name_column == 'xp_left_hand':
            user.xp_left_hand = current_value
        elif name_column == 'right_hand':
            user.right_hand = current_value
        elif name_column == 'xp_right_hand':
            user.xp_right_hand = current_value

        await session.commit()


async def set_storage_trash(tg_id: int, name_column: str, current_value: int, ) -> StorageTrash:
    logging.info(f'set_storage_trash')
    async with async_session() as session:
        storage_trash: StorageTrash = await session.scalar(select(StorageTrash).where(StorageTrash.tg_id == tg_id))
        #if name_column == 'bio':
        #    storage_trash.bio = current_value
        if name_column == 'f_aid':
            storage_trash.f_aid = current_value
        elif name_column == 'f_aid_s':
            storage_trash.f_aid_s = current_value
        elif name_column == 'bandages':
            storage_trash.bandages = current_value
        elif name_column == 'bandages_s':
            storage_trash.bandages_s = current_value
        elif name_column == 'canned_meat':
            storage_trash.canned_meat = current_value
        elif name_column == 'fried_meat':
            storage_trash.fried_meat = current_value
        elif name_column == 'fried_veins':
            storage_trash.fried_veins = current_value
        elif name_column == 'berries':
            storage_trash.berries = current_value
        elif name_column == 'bones':
            storage_trash.bones = current_value
        elif name_column == 'veins':
            storage_trash.veins = current_value
        elif name_column == 'vine_leaves':
            storage_trash.vine_leaves = current_value
        elif name_column == 'yel_fl':
            storage_trash.yel_fl = current_value
        elif name_column == 'stick':
            storage_trash.stick = current_value
        elif name_column == 'raw_meat':
            storage_trash.raw_meat = current_value
        elif name_column == 'seed_zlg':
            storage_trash.seed_zlg = current_value

        await session.commit()


async def set_storage_wardrobe(tg_id: int, name_column: str, current_value: str, ) -> StorageWardrobe:

    logging.info(f'set_storage_wardrobe')
    async with async_session() as session:
        storage_gun: StorageWardrobe = await session.scalar(select(StorageWardrobe).where(StorageWardrobe.tg_id == tg_id))
        if name_column == 'helmet_kosmonavt':
            storage_gun.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            storage_gun.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            storage_gun.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            storage_gun.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            storage_gun.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            storage_gun.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            storage_gun.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            storage_gun.shoes_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            storage_gun.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            storage_gun.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            storage_gun.backpack_leana = current_value

        await session.commit()



async def set_storage_gun(tg_id: int, name_column: str, current_value: int, ) -> StorageGun:

    logging.info(f'set_storage_gun')
    async with async_session() as session:
        storage_gun: StorageGun = await session.scalar(select(StorageGun).where(StorageGun.tg_id == tg_id))

        if name_column == 'G17':
            storage_gun.G17 = current_value
        elif name_column == 'spear':
            storage_gun.spear = current_value
        elif name_column == 'nothink':
            storage_gun.nothink = current_value
        await session.commit()

async def set_storage_bio(tg_id: int, name_column: str, current_value: int, ) -> StorageBIO:

    logging.info(f'set_storage_bio')
    async with async_session() as session:
        storage_bio: StorageBIO = await session.scalar(select(StorageBIO).where(StorageBIO.tg_id == tg_id))
        if name_column == 'bio':
            storage_bio.bio = current_value
        await session.commit()

async def set_backpack_foliage (tg_id: int, name_column: str, current_value: int, ) -> BackpackFoliage:
    logging.info(f'set_backpack_foliage')
    async with async_session() as session:
        backpack_foliage: BackpackFoliage = await session.scalar(select(BackpackFoliage).where(BackpackFoliage.tg_id == tg_id))

        if name_column == 'cell_1':
            backpack_foliage.cell_1 = current_value
        elif name_column == 'cell_2':
            backpack_foliage.cell_2 = current_value

        elif name_column == 'clb_back':
            backpack_foliage.clb_back = current_value
        elif name_column == 'bio':
            backpack_foliage.bio = current_value

        await session.commit()

async def set_b_foliage_cell_1(tg_id: int, name_column: str, current_value: int, ) -> BFoliageCell_1:
    logging.info(f'set_b_foliage_cell_1')
    async with async_session() as session:
        cell_1: BFoliageCell_1 = await session.scalar(select(BFoliageCell_1).where(BFoliageCell_1.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_1.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_1.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_1.bandages = current_value
        elif name_column == 'bandages_s':
            cell_1.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_1.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_1.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_1.fried_veins = current_value
        elif name_column == 'berries':
            cell_1.berries = current_value
        elif name_column == 'bones':
            cell_1.bones = current_value
        elif name_column == 'veins':
            cell_1.veins = current_value
        elif name_column == 'vine_leaves':
            cell_1.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_1.yel_fl = current_value
        elif name_column == 'stick':
            cell_1.stick = current_value
        elif name_column == 'raw_meat':
            cell_1.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_1.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_1.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_1.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_1.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_1.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_1.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_1.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_1.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_1.helmet_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_1.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_1.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_1.backpack_leana = current_value
        elif name_column == 'G17':
            cell_1.G17 = current_value
        elif name_column == 'spear':
            cell_1.spear = current_value
        elif name_column == 'nothink':
            cell_1.nothink = current_value
        await session.commit()

async def set_b_foliage_cell_2(tg_id: int, name_column: str, current_value: int, ) -> BFoliageCell_2:
    logging.info(f'set_b_foliage_cell_2')
    async with async_session() as session:
        cell_2: BFoliageCell_2 = await session.scalar(select(BFoliageCell_2).where(BFoliageCell_2.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_2.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_2.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_2.bandages = current_value
        elif name_column == 'bandages_s':
            cell_2.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_2.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_2.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_2.fried_veins = current_value
        elif name_column == 'berries':
            cell_2.berries = current_value
        elif name_column == 'bones':
            cell_2.bones = current_value
        elif name_column == 'veins':
            cell_2.veins = current_value
        elif name_column == 'vine_leaves':
            cell_2.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_2.yel_fl = current_value
        elif name_column == 'stick':
            cell_2.stick = current_value
        elif name_column == 'raw_meat':
            cell_2.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_2.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_2.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_2.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_2.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_2.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_2.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_2.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_2.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_2.helmet_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_2.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_2.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_2.backpack_leana = current_value
        elif name_column == 'G17':
            cell_2.G17 = current_value
        elif name_column == 'spear':
            cell_2.spear = current_value
        elif name_column == 'nothink':
            cell_2.nothink = current_value
        await session.commit()


async def set_backpack_leana (tg_id: int, name_column: str, current_value: int, ) -> BackpackLeana:
    logging.info(f'set_backpack_leana')
    async with async_session() as session:
        backpack_leana: BackpackLeana = await session.scalar(select(BackpackLeana).where(BackpackLeana.tg_id == tg_id))

        if name_column == 'cell_1':
            backpack_leana.cell_1 = current_value
        elif name_column == 'cell_2':
            backpack_leana.cell_2 = current_value
        elif name_column == 'cell_3':
            backpack_leana.cell_3 = current_value
        elif name_column == 'cell_4':
            backpack_leana.cell_4 = current_value

        elif name_column == 'xp':
            backpack_leana.xp = current_value
        elif name_column == 'bio':
            backpack_leana.bio = current_value

        await session.commit()

async def set_b_leana_cell_1(tg_id: int, name_column: str, current_value: int, ) -> BLeanaCell_1:
    logging.info(f'set_b_leana_cell_1')
    async with async_session() as session:
        cell_1: BLeanaCell_1 = await session.scalar(select(BLeanaCell_1).where(BLeanaCell_1.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_1.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_1.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_1.bandages = current_value
        elif name_column == 'bandages_s':
            cell_1.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_1.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_1.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_1.fried_veins = current_value
        elif name_column == 'berries':
            cell_1.berries = current_value
        elif name_column == 'bones':
            cell_1.bones = current_value
        elif name_column == 'veins':
            cell_1.veins = current_value
        elif name_column == 'vine_leaves':
            cell_1.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_1.yel_fl = current_value
        elif name_column == 'stick':
            cell_1.stick = current_value
        elif name_column == 'raw_meat':
            cell_1.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_1.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_1.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_1.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_1.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_1.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_1.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_1.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_1.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_1.shoes_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_1.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_1.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_1.backpack_leana = current_value
        elif name_column == 'G17':
            cell_1.G17 = current_value
        elif name_column == 'spear':
            cell_1.spear = current_value
        elif name_column == 'nothink':
            cell_1.nothink = current_value
        await session.commit()

async def set_b_leana_cell_2(tg_id: int, name_column: str, current_value: int, ) -> BLeanaCell_2:
    logging.info(f'set_b_leana_cell_2')
    async with async_session() as session:
        cell_: BLeanaCell_2 = await session.scalar(select(BLeanaCell_2).where(BLeanaCell_2.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_.bandages = current_value
        elif name_column == 'bandages_s':
            cell_.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_.fried_veins = current_value
        elif name_column == 'berries':
            cell_.berries = current_value
        elif name_column == 'bones':
            cell_.bones = current_value
        elif name_column == 'veins':
            cell_.veins = current_value
        elif name_column == 'vine_leaves':
            cell_.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_.yel_fl = current_value
        elif name_column == 'stick':
            cell_.stick = current_value
        elif name_column == 'raw_meat':
            cell_.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_.shoes_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_.backpack_leana = current_value
        elif name_column == 'G17':
            cell_.G17 = current_value
        elif name_column == 'spear':
            cell_.spear = current_value
        elif name_column == 'nothink':
            cell_.nothink = current_value
        await session.commit()

async def set_b_leana_cell_3(tg_id: int, name_column: str, current_value: int, ) -> BLeanaCell_3:
    logging.info(f'set_b_leana_cell_3')
    async with async_session() as session:
        cell_: BLeanaCell_3 = await session.scalar(select(BLeanaCell_3).where(BLeanaCell_3.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_.bandages = current_value
        elif name_column == 'bandages_s':
            cell_.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_.fried_veins = current_value
        elif name_column == 'berries':
            cell_.berries = current_value
        elif name_column == 'bones':
            cell_.bones = current_value
        elif name_column == 'veins':
            cell_.veins = current_value
        elif name_column == 'vine_leaves':
            cell_.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_.yel_fl = current_value
        elif name_column == 'stick':
            cell_.stick = current_value
        elif name_column == 'raw_meat':
            cell_.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_.shoes_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_.backpack_leana = current_value
        elif name_column == 'G17':
            cell_.G17 = current_value
        elif name_column == 'spear':
            cell_.spear = current_value
        elif name_column == 'nothink':
            cell_.nothink = current_value
        await session.commit()

async def set_b_leana_cell_4(tg_id: int, name_column: str, current_value: int, ) -> BLeanaCell_4:
    logging.info(f'set_b_leana_cell_4')
    async with async_session() as session:
        cell_: BLeanaCell_4 = await session.scalar(select(BLeanaCell_4).where(BLeanaCell_4.tg_id == tg_id))

        if name_column == 'f_aid':
            cell_.f_aid = current_value
        elif name_column == 'f_aid_s':
            cell_.f_aid_s = current_value
        elif name_column == 'bandages':
            cell_.bandages = current_value
        elif name_column == 'bandages_s':
            cell_.bandages_s = current_value
        elif name_column == 'canned_meat':
            cell_.canned_meat = current_value
        elif name_column == 'fried_meat':
            cell_.fried_meat = current_value
        elif name_column == 'fried_veins':
            cell_.fried_veins = current_value
        elif name_column == 'berries':
            cell_.berries = current_value
        elif name_column == 'bones':
            cell_.bones = current_value
        elif name_column == 'veins':
            cell_.veins = current_value
        elif name_column == 'vine_leaves':
            cell_.vine_leaves = current_value
        elif name_column == 'yel_fl':
            cell_.yel_fl = current_value
        elif name_column == 'stick':
            cell_.stick = current_value
        elif name_column == 'raw_meat':
            cell_.raw_meat = current_value
        elif name_column == 'seed_zlg':
            cell_.seed_zlg = current_value

        elif name_column == 'helmet_kosmonavt':
            cell_.helmet_kosmonavt = current_value
        elif name_column == 'helmet_wanderer':
            cell_.helmet_wanderer = current_value
        elif name_column == 'helmet_reinforced':
            cell_.helmet_reinforced = current_value
        elif name_column == 'dress_kosmonavt':
            cell_.dress_kosmonavt = current_value
        elif name_column == 'dress_wanderer':
            cell_.dress_wanderer = current_value
        elif name_column == 'dress_reinforced':
            cell_.dress_reinforced = current_value
        elif name_column == 'shoes_kosmonavt':
            cell_.shoes_kosmonavt = current_value
        elif name_column == 'shoes_wanderer':
            cell_.shoes_wanderer = current_value
        elif name_column == 'shoes_reinforced':
            cell_.shoes_reinforced = current_value
        elif name_column == 'backpack_foliage':
            cell_.backpack_foliage = current_value
        elif name_column == 'backpack_leana':
            cell_.backpack_leana = current_value
        elif name_column == 'G17':
            cell_.G17 = current_value
        elif name_column == 'spear':
            cell_.spear = current_value
        elif name_column == 'nothink':
            cell_.nothink = current_value
        await session.commit()

async def set_pocket1 (tg_id: int, name_column: str, current_value: int, ) -> Pocket1:
    logging.info(f'set_pocket1')
    async with async_session() as session:
        pocket1: Pocket1 = await session.scalar(select(Pocket1).where(Pocket1.tg_id == tg_id))
        if name_column == 'f_aid':
            pocket1.f_aid = current_value
        elif name_column == 'f_aid_s':
            pocket1.f_aid_s = current_value
        elif name_column == 'bandages':
            pocket1.bandages = current_value
        elif name_column == 'bandages_s':
            pocket1.bandages_s = current_value
        elif name_column == 'canned_meat':
            pocket1.canned_meat = current_value
        elif name_column == 'fried_meat':
            pocket1.fried_meat = current_value
        elif name_column == 'fried_veins':
            pocket1.fried_veins = current_value
        elif name_column == 'berries':
            pocket1.berries = current_value

        await session.commit()

async def set_pocket2 (tg_id: int, name_column: str, current_value: int, ) -> Pocket2:
    logging.info(f'set_pocket2')
    async with async_session() as session:
        pocket1: Pocket2 = await session.scalar(select(Pocket2).where(Pocket2.tg_id == tg_id))
        if name_column == 'f_aid':
            pocket1.f_aid = current_value
        elif name_column == 'f_aid_s':
            pocket1.f_aid_s = current_value
        elif name_column == 'bandages':
            pocket1.bandages = current_value
        elif name_column == 'bandages_s':
            pocket1.bandages_s = current_value
        elif name_column == 'canned_meat':
            pocket1.canned_meat = current_value
        elif name_column == 'fried_meat':
            pocket1.fried_meat = current_value
        elif name_column == 'fried_veins':
            pocket1.fried_veins = current_value
        elif name_column == 'berries':
            pocket1.berries = current_value

        await session.commit()



async def set_backpack_and_cell_with_chek_put_on_backpack (tg_id: int, cell: str|None=None, name_column_cell: str|None=None, current_value_cell: int|str|None=None):
    """ Установка значений во все b_foliage_cell_1, 2 ... b_leana_cell_1, 2, 3, 4... А также в pocket1 или pocket2"""
    logging.info(f'set_backpack_and_cell_with_chek_put_on_backpack') #"""name_column_backpack: str|None=None, current_value_backpack: int|str|None=None,""" это я вырезал выше и теперь эта функция не меняет Таблицы с рюкзаками


### ЕСТЬ ИДЕЯ ПЕРЕПИСАТЬ ЭТУ ФУНКЦИЮ. Не использовать рюкзаки. Только ячейки

    # Проверка какой рюкзак надет
    data_ = await get_user_dict(tg_id=tg_id)
    if '!' in data_['backpack']:
        backpack = data_['backpack'].split('!')[0]
    else:
        backpack = data_['backpack']

    if isinstance(name_column_cell, int|str) and isinstance(current_value_cell, int|str) and cell=='pocket1':
        await set_pocket1(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
    elif isinstance(name_column_cell, int|str) and isinstance(current_value_cell, int|str) and cell=='pocket2':
        await set_pocket2(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)


    if backpack == 'no_backpack':
        logging.info(f"set_backpack_and_cell_with_chek_put_on_backpack --- if backpack == 'no_backpack':")

    elif backpack == 'backpack_foliage': # если надет лиственный рюкзак
        #if isinstance(name_column_backpack, int|str) and isinstance(current_value_backpack, int|str): # в рюкзак устанавливаем только если передали эти значения
        #    await set_backpack_foliage(tg_id=tg_id, name_column=name_column_backpack, current_value=current_value_backpack)

        if isinstance(name_column_cell, int|str) and isinstance(current_value_cell, int|str):# в ячейки устанавливаем только если передали эти значения
            if cell=='cell_1':
                await set_b_foliage_cell_1(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
            elif cell=='cell_2':
                await set_b_foliage_cell_2(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)

    elif backpack == 'backpack_leana': # если надет леанный рюкзак
        #if isinstance(name_column_backpack, int|str) and isinstance(current_value_backpack, int|str): # в рюкзак устанавливаем только если передали эти значения
        #    await set_backpack_leana(tg_id=tg_id, name_column=name_column_backpack, current_value=current_value_backpack)

        if isinstance(name_column_cell, int|str) and isinstance(current_value_cell, int|str):# в ячейки устанавливаем только если передали эти значения
            if cell=='cell_1':
                await set_b_leana_cell_1(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
            elif cell=='cell_2':
                await set_b_leana_cell_2(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
            elif cell=='cell_3':
                await set_b_leana_cell_3(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
            elif cell=='cell_4':
                await set_b_leana_cell_4(tg_id=tg_id, name_column=name_column_cell, current_value=current_value_cell)
