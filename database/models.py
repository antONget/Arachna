from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    xp: Mapped[int] = mapped_column(Integer, default=98)

    ###Эти два должны тут лежать или где-то ниже в ящиках?
    kristals: Mapped[int] = mapped_column(Integer, default=5)
    location: Mapped[str] = mapped_column(String, default='landing_place')
    time: Mapped[str] = mapped_column(String, default='')

### Скорее всего я перепишу названия этих ячеек -- это буде оружие
# в начале игры есть G17, а второе оружие - отсутствует
    #pocket1: Mapped[int] = mapped_column(Integer, default=0)
    #pocket2: Mapped[int] = mapped_column(Integer, default=0)

    backpack: Mapped[str] = mapped_column(String, default='no_backpack')
    xp_backpack: Mapped[int] = mapped_column(Integer, default=0)
    #другие два значения: 'backpack_foliage' backpack_leana'

    helmet: Mapped[str] = mapped_column(String, default='helmet_kosmonavt!5')
    xp_helmet: Mapped[int] = mapped_column(Integer, default=250)
    #другие значения: 'helmet_kosmonavt', 'helmet_wanderer', 'helmet_reinforced'

    dress: Mapped[str] = mapped_column(String, default='dress_kosmonavt!5')
    xp_dress: Mapped[int] = mapped_column(Integer, default=275)
    shoes: Mapped[str] = mapped_column(String, default='shoes_kosmonavt!5')
    xp_shoes: Mapped[int] = mapped_column(Integer, default=200)

    left_hand: Mapped[str] = mapped_column(String, default='G17!30') # название_оружия!ХП
    xp_left_hand: Mapped[int] = mapped_column(Integer, default=6)
    right_hand: Mapped[str] = mapped_column(String, default='') # G17 spear '' nothink
    xp_right_hand: Mapped[int] = mapped_column(Integer, default=0)

class StorageTrash(Base):
    __tablename__ = 'storage_trash'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=3)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=5)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=5)# тушенка
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0) # жилы
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

class StorageWardrobe(Base):  # "!0!98!44!0" через строку показано сколько вещей с разными процентами есть
    __tablename__ = 'storage_wardrobe'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    helmet_kosmonavt: Mapped[int] = mapped_column(String, default='')
    helmet_wanderer: Mapped[int] = mapped_column(String, default='')
    helmet_reinforced: Mapped[int] = mapped_column(String, default='')

    dress_kosmonavt: Mapped[int] = mapped_column(String, default='')
    dress_wanderer: Mapped[int] = mapped_column(String, default='')
    dress_reinforced: Mapped[int] = mapped_column(String, default='')

    shoes_kosmonavt: Mapped[int] = mapped_column(String, default='')
    shoes_wanderer: Mapped[int] = mapped_column(String, default='')
    shoes_reinforced: Mapped[int] = mapped_column(String, default='')

    backpack_foliage: Mapped[int] = mapped_column(String, default='')
    backpack_leana: Mapped[int] = mapped_column(String, default='')

class StorageGun(Base):
    __tablename__ = 'storage_gun'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    G17: Mapped[int] = mapped_column(String, default='')
    spear: Mapped[int] = mapped_column(String, default='')
    nothink: Mapped[int] = mapped_column(String, default='')

class StorageBIO(Base):
    __tablename__ = 'storage_bio'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    bio: Mapped[int] = mapped_column(Integer, default=0)


class BackpackFoliage(Base):
    __tablename__ = 'backpack_foliage'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    cell_1: Mapped[int] = mapped_column(Integer, default=0)
    cell_2: Mapped[int] = mapped_column(Integer, default=0)

    clb_back: Mapped[int] = mapped_column(String, default='')
    bio: Mapped[int] = mapped_column(Integer, default=0)

class BFoliageCell_1(Base):
    __tablename__ = 'b_foliage_cell_1'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)###уточнить какой бинт (бинт или бинт простой)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)# тушенка
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0) # жилы
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class BFoliageCell_2(Base):
    __tablename__ = 'b_foliage_cell_2'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)###уточнить какой бинт (бинт или бинт простой)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)# тушенка
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0)
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class BackpackLeana(Base):
    __tablename__ = 'backpack_leana'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    cell_1: Mapped[int] = mapped_column(Integer, default=0)
    cell_2: Mapped[int] = mapped_column(Integer, default=0)
    cell_3: Mapped[int] = mapped_column(Integer, default=0)
    cell_4: Mapped[int] = mapped_column(Integer, default=0)

    xp: Mapped[int] = mapped_column(Integer, default=150)
    bio: Mapped[int] = mapped_column(Integer, default=0)

class BLeanaCell_1(Base):
    __tablename__ = 'b_leana_cell_1'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0)
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class BLeanaCell_2(Base):
    __tablename__ = 'b_leana_cell_2'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0)
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class BLeanaCell_3(Base):
    __tablename__ = 'b_leana_cell_3'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0)
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class BLeanaCell_4(Base):
    __tablename__ = 'b_leana_cell_4'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

    bones: Mapped[int] = mapped_column(Integer, default=0)
    veins: Mapped[int] = mapped_column(Integer, default=0)
    vine_leaves: Mapped[int] = mapped_column(Integer, default=0)
    yel_fl: Mapped[int] = mapped_column(Integer, default=0)
    stick: Mapped[int] = mapped_column(Integer, default=0)
    raw_meat: Mapped[int] = mapped_column(Integer, default=0)
    seed_zlg: Mapped[int] = mapped_column(Integer, default=0)

    helmet_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    helmet_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    helmet_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    dress_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    dress_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    dress_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    shoes_kosmonavt: Mapped[int] = mapped_column(Integer, default=0)
    shoes_wanderer: Mapped[int] = mapped_column(Integer, default=0)
    shoes_reinforced: Mapped[int] = mapped_column(Integer, default=0)

    backpack_foliage: Mapped[int] = mapped_column(Integer, default=0)
    backpack_leana: Mapped[int] = mapped_column(Integer, default=0)

    G17: Mapped[int] = mapped_column(Integer, default=0)
    spear: Mapped[int] = mapped_column(Integer, default=0)
    nothink: Mapped[int] = mapped_column(Integer, default=0)

class Pocket1(Base):
    __tablename__ = 'pocket_1'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)# тушенка
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)

class Pocket2(Base):
    __tablename__ = 'pocket_2'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String, default='username')

    f_aid: Mapped[int] = mapped_column(Integer, default=0)
    f_aid_s: Mapped[int] = mapped_column(Integer, default=0)
    bandages: Mapped[int] = mapped_column(Integer, default=0)
    bandages_s: Mapped[int] = mapped_column(Integer, default=0)
    canned_meat: Mapped[int] = mapped_column(Integer, default=0)# тушенка
    fried_meat: Mapped[int] = mapped_column(Integer, default=0)
    fried_veins: Mapped[int] = mapped_column(Integer, default=0)
    berries: Mapped[int] = mapped_column(Integer, default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)