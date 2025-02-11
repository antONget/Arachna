from aiogram.types import Message, CallbackQuery, InputMediaPhoto
import logging
import database.requests as rq
from lexicon.foto import PHOTO as ph
import keyboards.keybords as kb
from dataclasses import dataclass


from lexicon.lexicon_ru import (list_storage_wardrobe_and_gun_and_craft as LSWGC,
                                list_storage_wardrobe_gun as LSWG,
                                list_storage_trash as LST,
                                list_storage_trash_drag as lstd,
                                list_storage_wardrobe as LSW,
                                list_storage_gun as LSG,
                                LEXICON_STORAGE_WARDROBE as LSW,
                                LEXICON_ALL_THINGS as All_Th,
                                dict_use_storage_trash as dict_u,
                                dict_armor, dict_gun, dict_NPS, dict_percent_xp)

@dataclass
class Backpack:
    no_backpack = "no_backpack"
    backpack_foliage = "backpack_foliage"
    backpack_leana = "backpack_leana"

@dataclass
class Location:
    landing_place = 'landing_place'
    # в пути
    # луга


# убирает из словаря ключи, значения которых равны 0
async def modify_dict_to_without_null (dict_ :dict) -> dict:
    logging.info(f'modify_dict_to_without_null')
    dict_modify: dict = {}
    for key in dict_:
        if dict_[key] != 0:
            dict_modify.update({key: dict_[key]})
    return dict_modify


# функция, которая получает строку типа '!100!13!97!13!100!0!0', а выдает словарь {100: 2, 97: 1, 13: 2}
# и СОРТИРУЕТ, и УБИРАЕТ НУЛИ, и ОБЪЕДЕНЯЕТ одинаковые значения в одном ключе
async def modify_str_to_dict (str_ :str) -> dict:
    #logging.info(f'modify_str_to_dict --- str_ = {str_}')
    dict_: dict = {}
    if str_ == 0 or str_ == '':
        return dict_
    #logging.info(f'modify_str_to_dict 1 dict_ = {dict_}')

    if isinstance(str_, str) and '!' in str_:
        list_ = str_.split('!')
    #  в некоторых строках отсутствует !, делать проверку на пустой первый элемент списка
        if not list_[0]: # ["", "1",...] - первый элемент при проверке на if == None
            list_.pop(0)
    else:
        list_ = [str_]
    #logging.info(f'modify_str_to_dict 1,5 list_ = {list_}')
    list_ = [int(value) for value in list_]
    list_.sort(reverse=True)
    #logging.info(f'modify_str_to_dict 2 list_ = {list_}')
    for value in list_:
        if value not in dict_ and value >0:
            dict_ [value] = 1
            #logging.info(f'modify_str_to_dict 3 dict_ = {dict_}')
        else:
            if value > 0:
                dict_[value]+=1
                #logging.info(f'modify_dict_to_without_null 4 dict_ = {dict_}')
    return dict_


# функция, которая из предыдущего словаря делает список списков. В списке два элемента: ключ, значение из словаря
# Это для реализации вывода из Хранилища шкаф только 5 элементов, и перехода далее и назад
async def modify_dict_to_list_of_list_of_2_elements(dict_: dict) -> list:
    #logging.info(f"modify_dict_to_list_of_list_of_2_elements --- dict_ = {dict_}")
    list_: list = []
    for key, item in dict_.items():
        list_temp: list = [key, item]
        list_.append(list_temp)
    #logging.info(f"modify_dict_to_list_of_list_of_2_elements --- list = {list_}")
    return list_


# функция, которая получает словарь {100: 2, 97: 1, 13: 2}, а выдает чило - сумму вещей
async def modify_dict_to_int_with_count_thinks_value(dict_: dict) -> int:
    #logging.info(f'modify_dict_to_int_with_count_thinks_value --- dict_ = {dict_}')
    int_: int = 0
    for value in dict_.values():
         int_ += value
    return int_


# из словаря {'helmet_kosmonavt': '', 'helmet_wanderer': '!0!98!44!0'} в словарь {'helmet_wanderer': 2}
async def modify_dict_to_dict_with_count_value(dict_: dict) -> dict:
    logging.info(f'modify_dict_to_dict_with_count_value')
    """# из словаря {'helmet_kosmonavt': '', 'helmet_wanderer': '!0!98!44!0'} в словарь {'helmet_wanderer': 2}"""

    dict_without_empty : dict ={}
    for key, value in dict_.items():
        dict_from_str: dict = await modify_str_to_dict(value)
        int_from_dict: int = await modify_dict_to_int_with_count_thinks_value(dict_from_str)
        if int_from_dict>0:
            dict_without_empty.update({key: int_from_dict})
    return dict_without_empty


# возвращает список какой рюкзак надет: bacpack_foliage, backpack_leana,
# no_backpack и сколько там био, для no_backpak = -1
async def bio_in_what_backpack_put_on(tg_id: int) -> list:
    """# возвращает список какой рюкзак надет: bacpack_foliage, backpack_leana,
        # no_backpack и сколько там био, для no_backpak = -1"""
    list_backpck_bio: list = [str, int]
    logging.info(f'bio_in_what_backpack_put_on')

    data_ = await rq.get_user_dict(tg_id=tg_id)
    backpack = data_['backpack']
    if backpack == Backpack.no_backpack:
        list_backpck_bio = [backpack, -1]
    elif backpack == Backpack.backpack_foliage:
        foliage = await rq.get_BackpackFoliage(tg_id=tg_id)
        bio = foliage['bio']
        list_backpck_bio = [backpack, bio]
    elif backpack == Backpack.backpack_leana:
        leana = await rq.get_BackpackLeana(tg_id=tg_id)
        bio = leana['bio']
        list_backpck_bio = [backpack, bio]
    return list_backpck_bio


# возвращает строку какой рюкзак надет: 'no_backpack', 'backpack_foliage', 'backpack_leana'
async def what_backpack_put_on(tg_id: int) -> str:
    """
    возвращает строку какой рюкзак надет: 'no_backpack', 'backpack_foliage', 'backpack_leana' без!
    """
    logging.info(f'what_backpack_put_on')
    backpack: str = Backpack.no_backpack   # по умолчанию "нет рюкзака", если есть переопределяем
    data_ = (await rq.get_user_dict(tg_id=tg_id))['backpack']
    if '!' in data_:
        if data_.split('!')[0] == Backpack.backpack_foliage:
            backpack = Backpack.backpack_foliage

        elif data_.split('!')[0] == Backpack.backpack_leana:
            backpack = Backpack.backpack_leana

    return backpack


# функция берет строку из wardrobe '!0!98!44!13!55' и убирает то число - (%),
# которое выбрал пользователь, заодно убирает нулевые значения
async def modify_str_to_str_del_choise_percent_and_null(str_from_database: str, choise_percent: str) -> str:
    """
    функция берет строку из wardrobe '!0!98!44!13!55' и убирает то число - (%),
    которое выбрал пользователь, заодно убирает нулевые значения
    """
    logging.info(f"modify_str_to_str_del_choise_percent_and_null --- str_from_database={str_from_database} --- choise_percent={choise_percent}")
    if '!' in str_from_database:
        list_:list = str_from_database.split('!')
        #logging.info(f"ВРЕМЕННО 1 --- list_ = {list_}")
        if not list_[0]: # Если впереди стоял ! и первый элемен после split стал ["", "1"], т.е. None
            list_.pop(0)

        #logging.info(f"ВРЕМЕННО 2 --- list_ = {list_} Проверь. строка уже отсортирована?")
        list_ = [int(value) for value in list_]
        list_.sort(reverse=True)
    else:
        list_:list = []
        if str_from_database:
            list_.append(int(str_from_database))

    # блок для удаления 0 из строки, может быть его перенести куда-то в другое место
    if 0 in list_:
        while 0 in list_:
            list_.remove(0)

    # Переводим обратно в строку
    list_ = [str(value) for value in list_]

    if choise_percent in list_:
        logging.info(f'choise_percent = {choise_percent}  -----  list_ = {list_}')
        list_.remove(choise_percent)
    # метод .join может собирать только строки
    str_return = '!'.join(list_)
    logging.info(f"ВРЕМЕННО 3 --- str_return = {str_return}")

    return str_return


# Возвращает список списков для клавиатуры с цветными кнопками
# при взаимодействии с Wardrobe, тут нет желтых ячеек
async def create_list_for_create_keyboard_with_colored_cell_without_yellow_cell(tg_id: int, prefix: str='') -> list:
    """
    ВНИМАНИЕ ПЕРЕПУТАНЫ МЕСТАМИ ЯЧЕЙКИ "ЦВЕТ" "РЮКЗАК"
    Возвращает список списков для клавиатуры с цветными кнопками,
    при взаимодействии с Wardrobe, тут нет желтых ячеек
    """
    logging.info(f"create_list_for_create_keyboard_with_colored_cell_without_yellow_cell")
    list_colored_button: list = []
    green = '🟩'
    yellow = '🟨'
    red = '🟥'
    backpack = await what_backpack_put_on(tg_id=tg_id) # на ! проверка есть

    if backpack == Backpack.no_backpack:
        return

    elif backpack == Backpack.backpack_foliage:
        #data_bf_cell = await rq.get_BackpackFoliage(tg_id=tg_id)
        #cell_1 = data_bf_cell['cell_1']
        #cell_2 = data_bf_cell['cell_2']

        dict_cell_1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        dict_cell_2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        logging.info(f"ВРЕМЕННО 1 --- dict_cell_1 = {dict_cell_1} --- dict_cell_2 = {dict_cell_2}")

        if not dict_cell_1: # одинарная проверка:  словарь с вещами должен быть пустой,
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_1'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_1'}"])

        if not dict_cell_2:
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_2'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_2'}"])
        logging.info(f"ВРЕМЕННО 2 --- list_colored_button = {list_colored_button}")

    elif backpack == Backpack.backpack_leana:
        #data_bl_cell = await rq.get_BackpackLeana(tg_id=tg_id)
        #cell_1 = data_bl_cell['cell_1']
        #cell_2 = data_bl_cell['cell_2']
        #cell_3 = data_bl_cell['cell_3']
        #cell_4 = data_bl_cell['cell_4']

        dict_cell_1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        dict_cell_2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        dict_cell_3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        dict_cell_4 = await rq.get_BLeanaCell_4(tg_id=tg_id)
        logging.info(f"ВРЕМЕННО 1 --- dict_cell_1 = {dict_cell_1} --- dict_cell_2 = {dict_cell_2} --- dict_cell_3 = {dict_cell_3} --- dict_cell_4 = {dict_cell_4}")

        if not dict_cell_1: # двойная проверка: и словарь с вещами должен быть пустой, и число в ячейке = 0
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_1'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_1'}"])

        if not dict_cell_2:
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_2'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_2'}"])

        if not dict_cell_3:
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_3'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_3'}"])

        if not dict_cell_4:
            list_colored_button.append([green, f"{prefix}!{'green'}!{backpack}!{'cell_4'}"])
        else:
            list_colored_button.append([red, f"{prefix}!{'red'}!{backpack}!{'cell_4'}"])

        logging.info(f"ВРЕМЕННО 2 --- list_colored_button = {list_colored_button}")
    return list_colored_button


# возвращает словарь всего того, что есть в рюкзаке
async def dict_with_all_things_from_backpack(tg_id: int, pocket: str|None=None) -> dict:
    """ # возвращает словарь всего того, что есть в рюкзаке, а если передан параметр 'pocket', то и в карманах"""
    logging.info('dict_with_all_things_from_backpack')

    backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
    common_dict: dict = {}

    pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    pocket2 = await rq.get_Pocket2(tg_id=tg_id)

    if backpack_put_on == Backpack.backpack_foliage:
        cell1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        cell2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        cell3 = 0
        cell4 = 0


    elif backpack_put_on == Backpack.backpack_leana:
        cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)


    # составляем общий словарь со всеми вещами из карманов и всех ячеек

    # чтобы добавить в выводимый словарь ПОКЕТЫ, надо передать на вход 'pocket'
    if pocket:
        if pocket1:
            if list(pocket1.keys())[0] not in list(common_dict.keys()):
                common_dict.update(pocket1)
            else:
                key = list(pocket1.keys())[0]
                if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                    common_dict.update({key: f"{common_dict[key]}!{pocket1[key]}"})
                else: # если вещь из трэша
                    common_dict.update({key: common_dict[key]+pocket1[key]})

        if pocket2:
            if list(pocket2.keys())[0] not in list(common_dict.keys()):
                common_dict.update(pocket2)
            else:
                key = list(pocket2.keys())[0]
                if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                    common_dict.update({key: f"{common_dict[key]}!{pocket2[key]}"})
                else: # если вещь из трэша
                    common_dict.update({key: common_dict[key]+pocket2[key]})

    if cell1:
        if list(cell1.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell1)
        else:
            key = list(cell1.keys())[0]
            if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                common_dict.update({key: f"{common_dict[key]}!{cell1[key]}"})
            else: # если вещь из трэша
                common_dict.update({key: common_dict[key]+cell1[key]})

    if cell2:
        if list(cell2.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell2)
        else:
            key = list(cell2.keys())[0]
            if key in LSWG:
                common_dict.update({key: f"{common_dict[key]}!{cell2[key]}"})
            else: # если
                common_dict.update({key: common_dict[key]+cell2[key]})

    if cell3:
        if list(cell3.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell3)
        else:
            key = list(cell3.keys())[0]
            if key in LSWG:
                common_dict.update({key: f"{common_dict[key]}!{cell3[key]}"})
            else: # если
                common_dict.update({key: common_dict[key]+cell3[key]})

    if cell4:
        if list(cell4.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell4)
        else:
            key = list(cell4.keys())[0]
            if key in LSWG:
                common_dict.update({key: f"{common_dict[key]}!{cell4[key]}"})
            else: # если
                common_dict.update({key: common_dict[key]+cell4[key]})

    logging.info(f'ВРЕМЕННО return --- dict_with_all_things_from_backpack --- {common_dict}')
    return common_dict



# берет словарь сверху и выдает строку с раздлителем \n для удобного вывода на экране всего того, что есть в словаре
async def modify_dict_with_all_things_from_backpack_to_srt_with_enter(dict_: dict) -> str:
    """ берет словарь сверху и выдает строку с раздлителем \n для удобного вывода на экране всего того, что есть в словаре"""
    logging.info('modify_dict_with_all_things_from_backpack_to_srt_with_enter')
    str_: str = ''
    for key, value in dict_.items():
        if key in LSWG:
            if '!' in str(value):
                list_ = value.split('!')
                for thing in list_:
                    str_ = str_ + f"{All_Th[key]} {thing}%\n"
            else:
                str_ = str_ + f"{All_Th[key]} {value}%\n"
        else:
            str_ = str_ + f"{All_Th[key]} {value}шт.\n"
    return str_

# возвращает список со словарями всего того, что есть в рюкзаке c указанием в каком(й) кармане\ячейке лежит эта вещь
async def create_list_with_dict_all_things_from_pocket_and_cell_backpack(tg_id: int) -> list[dict]:
    """ # возвращает список со словарями всего того, что есть в рюкзаке c указанием в каком(й) кармане\ячейке лежит эта вещь """
    logging.info('create_list_with_dict_all_things_from_pocket_and_cell_backpack')

    backpack_put_on = await what_backpack_put_on(tg_id=tg_id)

    list_return: list[list,list,list] = [[],[],[]]

    pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    if pocket1:
        list_return[0].append({'pocket1': pocket1})
        list_return[1].append(list(pocket1.keys())[0])
        list_return[2].append('pocket1')

    pocket2 = await rq.get_Pocket2(tg_id=tg_id)
    if pocket2:
        list_return[0].append({'pocket2': pocket2})
        list_return[1].append(list(pocket1.keys())[0])
        list_return[2].append('pocket2')

    if backpack_put_on == Backpack.backpack_foliage:
        cell1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        cell2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        cell3 = 0
        cell4 = 0

    elif backpack_put_on == Backpack.backpack_leana:
        cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)

    if cell1:
        list_return[0].append({'cell1': cell1})
        list_return[1].append(list(cell1.keys())[0])
        list_return[2].append('cell1')
    if cell2:
        list_return[0].append({'cell2': cell2})
        list_return[1].append(list(cell2.keys())[0])
        list_return[2].append('cell2')
    if cell3:
        list_return[0].append({'cell3': cell3})
        list_return[1].append(list(cell3.keys())[0])
        list_return[2].append('cell3')
    if cell4:
        list_return[0].append({'cell4': cell4})
        list_return[1].append(list(cell4.keys())[0])
        list_return[2].append('cell4')

    logging.info(f'list_return = {list_return}')
    return list_return


# Проверяет может ли весь найденный лут переместиться в карманы и ячейки надетого рюкзака, если да, то распихивает по карманам и ячейкам
async def check_all_loot_put_on_pockets_and_cells_backpack_if_yes_remove(tg_id:int, dict_loot: dict) -> bool:
    """ Проверяет может ли весь найденный лут переместиться в карманы и ячейки надетого рюкзака, если да, то распихивает по карманам и ячейкам """
    logging.info('check_all_loot_put_on_pockets_and_cells_backpack_if_yes_remove(dict_loot: dict) -> bool:')

    # спрашиваем какой рюкзак надет, если нет рюкзака, то return false
    backpack = await what_backpack_put_on(tg_id)
    if backpack == 'no_backpack':
        return False

    #list_pocket_cell:list = await create_list_with_dict_all_things_from_pocket_and_cell_backpack(tg_id=tg_id)
    #найденный лут 'berries'= 4, 'vine_leaves'=1, 'yel_fl'=2, 'stick'=3, 'seed_zlg'=1

    # list_dict_p_c ##### list_return = [[{'pocket1': {'berries': 10}}, {'cell2': {'shoes_wanderer': 34}}, {'cell3': {'seed_zlg': 19}}],
    # ['berries', 'shoes_wanderer', 'seed_zlg'], ['pocket1', 'cell2', 'cell3']]

   # for key, value in dict_loot.items():
     #   if

#    dict_pocket_cell:dict = await dict_with_all_things_from_backpack(tg_id=tg_id, pocket='pocket')
#    list_dict_p_c = await create_list_with_dict_all_things_from_pocket_and_cell_backpack(tg_id)
#    temp_list_dict_p_c: list = []
#    list_name_pocket_cell = ['pocket1', 'pocket2', 'cell1', 'cell2', 'cell3', 'cell4']
#    count_list_name_p_c: int = 0
#    for name_p_c in list_name_pocket_cell: # проходим по списку list_name_pocket_cell = ['pocket1', 'pocket2', 'cell1', 'cell2', 'cell3', 'cell4']
#        if name_p_c in list_dict_p_c[2]: # если он есть есть в list_dict_p_c = await create_list_with_dict_all_things_from_pocket_and_cell_backpack(tg_id) [2]

#            for elem in list_dict_p_c[0]: # то перебираем словари с ключами
#                if name_p_c == list(elem.keys())[0]: # ищем его и
#                    temp_list_dict_p_c.append(elem) # добавляем в новый список
#        else:
#            temp_list_dict_p_c.append({list_name_pocket_cell[count_list_name_p_c]: {}})
#        count_list_name_p_c+=1

    # temp_list_dict_p_c = [{'pocket1': {}}, {'pocket2': {}}, {'cell1': {}}, {'cell2': {'shoes_wanderer': 34}}, {'cell3': {'seed_zlg': 19}}, {'cell4': {}}]
    # 1 проходим по элементам налутованных вещей
#    flag: bool = True
#    len_dict_loot = len(dict_loot) # длина словаря с лутом

#    for loot, value_loot in dict_loot.items(): # {'berries': 2, 'vine_leaves': 1, 'yel_fl': 3, 'stick': 3, 'seed_zlg': 1}
#        if loot not in list_dict_p_c[1]: # если единица лута НЕТ в списке карманы-ячейки
#            # отдельная проверка для ягод, они могут быть перемещены в карманы, другое нет
#            if loot == 'berries':
#                count_ = 0
#                for dict_elem in temp_list_dict_p_c[:]: # [{'pocket1': {}}, {'pocket2': {}}, {'cell1': {}}, {'cell2': {'shoes_wanderer': 34}},
#                    name_pc = list(dict_elem.keys())[0]
#                    if not dict_elem[name_pc]:   # если не существует, то записать {'cell2': {'shoes_wanderer': 34} == False --- {'pocket2': {}} == True
#                        temp_list_dict_p_c[count_][name_pc]={loot: value_loot}
#                    else:
#                        count_+=1
#            else:
#                count_ = 0
#                for dict_elem in temp_list_dict_p_c[2:]: # [{'pocket1': {}}, {'pocket2': {}}, {'cell1': {}}, {'cell2': {'shoes_wanderer': 34}},
#                    name_pc, dict_pc = dict_elem.items()
#                    if not dict_elem[name_pc]:   # если не существует, то записать {'cell2': {'shoes_wanderer': 34} == False --- {'pocket2': {}} == True
#                        temp_list_dict_p_c[count_][name_pc]={loot: value_loot}
#                    else:
#                        count_+=1
#            logging.info(f'\ndict_loot = {dict_loot}\ndict_pocket_cell = {dict_pocket_cell}\nlist_dict_p_c = {list_dict_p_c}\ntemp_list_dict_p_c = {temp_list_dict_p_c}')

#        else:  # если единица лута ЕСТЬ в списке карманы-ячейки
            # ищем в каком словаре этот лут
            #for dict_elem in temp_list_dict_p_c[:]: # [{'pocket1': {}}, {'pocket2': {}}, {'cell1': {}}, {'cell2': {'shoes_wanderer': 34}},
             #   name_pc, dict_pc = dict_elem.items()
              #  if not dict_elem[name_pc]:   # если не существует, то записать {'cell2': {'shoes_wanderer': 34} == False --- {'pocket2': {}} == True
#            logging.info(f'else')








                #for elem_dict in list_dict_p_c: # [{'cell2': {'shoes_wanderer': 34}}, {'cell3': {'seed_zlg': 19}}]
                 #   pocket_cell, dict_name_value_p_c = elem_dict.items()
                  #  name_loot, value









#        logging.info(f'\ndict_loot = {dict_loot}\ndict_pocket_cell = {dict_pocket_cell}\nlist_dict_p_c = {list_dict_p_c}\ntemp_list_dict_p_c = {temp_list_dict_p_c}')
    return True
    #

    # объединяем два словаря

#    for key, value in dict_loot.items():
#
#        if key in list(dict_pocket_cell.keys()):
#            dict_pocket_cell.update({key: dict_pocket_cell[key]+value})
#        else:
#            dict_pocket_cell.update({key: value})
#    logging.info(f'common_dict = {dict_pocket_cell}')

    # Проверим сколько в новом словаре ключей (вещей) у которых значения больше 20
#    count_value_more_20: int = 0
#    for key, value in dict_pocket_cell.items():
#        if value > 20 and key not in LSWG:
#            count_value_more_20 += 1

#    if backpack == Backpack.backpack_leana:
#        if len(dict_pocket_cell)>6 or (len(dict_pocket_cell)>5 and count_value_more_20>0) or (len(dict_pocket_cell)>4 and count_value_more_20>1) or (len(dict_pocket_cell)
#            >3 and count_value_more_20>2):
#            logging.info(f'len(dict_pocket_cell) = {len(dict_pocket_cell)}--- dict_pocket_cell={dict_pocket_cell} --- count_value_more_20 = {count_value_more_20}')
#            return False
#        else:
#            logging.info(f'Будет возвращено ТРУ леанный рюкзак')

#    elif backpack == Backpack.backpack_foliage:
#        if len(dict_pocket_cell)>4 or (len(dict_pocket_cell)>3 and count_value_more_20>0) or (len(dict_pocket_cell)>2 and count_value_more_20>1) or (len(dict_pocket_cell)
#            >1 and count_value_more_20>2):
#            return False
#        else:
#            logging.info(f'Будет возвращено ТРУ лиственный рюкзак')

    # тут сделать перекидку вещей из онайденного лута в надетый рюкзак









# all_things_can_be_moved_to_a_new_backpack --- Возвращает True, или если был надет лиственный рюкзак,
# или вещи из леанного рюкзака помещаются в лиственный
async def all_things_can_be_moved_to_a_new_backpack(tg_id: int) -> bool:
    """
    Возвращает True, или если был надет лиственный рюкзак, или вещи из леанного рюкзака помещаются в лиственный. Ничего не перемещает.
    """
    logging.info(f"all_things_can_be_moved_to_a_new_backpack")

    data_backpack_foliage = await rq.get_BackpackFoliage(tg_id=tg_id)
    data_backpack_leana = await rq.get_BackpackLeana(tg_id=tg_id)
    backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
    logging.info(f" ВРЕМЕННО --- all_things_can_be_moved_to_a_new_backpack --- backpack_put_on = {backpack_put_on}")

    if backpack_put_on == Backpack.no_backpack:
        return False
    elif backpack_put_on == Backpack.backpack_foliage:
        return True
    elif backpack_put_on == Backpack.backpack_leana:
        # делаем проверку на то, помястятся ли вещи в лиственный рюкзак
        data_bl_cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        data_bl_cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        data_bl_cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        data_bl_cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)
        common_dict: dict = {}

        if data_bl_cell1:
            if list(data_bl_cell1.keys())[0] not in list(common_dict.keys()):
                common_dict.update(data_bl_cell1)
            else:
                key = list(data_bl_cell1.keys())[0]
                common_dict.update({key: common_dict[key]+data_bl_cell1[key]})
        #logging.info(f" data_bl_cell1 = {data_bl_cell1} --- common_dict = {common_dict}"
         #            f"\n len(list(common_dict.keys())) = {len(list(common_dict.keys()))} --- list(common_dict.values()) = {list(common_dict.values())}")

        if data_bl_cell2:
            if list(data_bl_cell2.keys())[0] not in list(common_dict.keys()):
                common_dict.update(data_bl_cell2)
            else:
                key = list(data_bl_cell2.keys())[0]
                common_dict.update({key: common_dict[key]+data_bl_cell2[key]})
        #logging.info(f" data_bl_cell2 = {data_bl_cell2} --- common_dict = {common_dict}"
         #            f"\n len(list(common_dict.keys())) = {len(list(common_dict.keys()))} --- list(common_dict.values()) = {list(common_dict.values())}")

        if data_bl_cell3:
            if list(data_bl_cell3.keys())[0] not in list(common_dict.keys()):
                common_dict.update(data_bl_cell3)
            else:
                key = list(data_bl_cell3.keys())[0]
                common_dict.update({key: common_dict[key]+data_bl_cell3[key]})
        #logging.info(f" data_bl_cell3 = {data_bl_cell1} --- common_dict = {common_dict}"
         #            f"\n len(list(common_dict.keys())) = {len(list(common_dict.keys()))} --- list(common_dict.values()) = {list(common_dict.values())}")

        if data_bl_cell4:
            if list(data_bl_cell4.keys())[0] not in list(common_dict.keys()):
                common_dict.update(data_bl_cell4)
            else:
                key = list(data_bl_cell4.keys())[0]
                common_dict.update({key: common_dict[key]+data_bl_cell4[key]})
        #logging.info(f" data_bl_cell4 = {data_bl_cell1} --- common_dict = {common_dict}"
         #            f"\n len(list(common_dict.keys())) = {len(list(common_dict.keys()))} --- list(common_dict.values()) = {list(common_dict.values())}")
        #   если есть ключи от более чем 2 ячеек               или заняты две ячейки, но в любой из ней больше 21                                                        или если одна ячейка, но более 40 вещей
        if len(list(common_dict.keys()))>2 or (len(list(common_dict.keys()))==2 and (list(common_dict.values())[0]>20 or list(common_dict.values())[1]>=20)) or (len(list(common_dict.keys()))==1 and list(common_dict.values())[0]>40):
            return False
        return True


# в надетом рюкзаке удаляет все вещи из всех ячеек
async def delete_all_things_from_put_on_backpack(tg_id: int, pocket: str|None=None, del_backpack_xp: str|None=None) -> None:
    """в надетом рюкзаке удаляет все вещи из всех ячеек, а если передан параметр 'pocket', то и в ячейках,
    если передан параметр 'del_backpack_xp' то удалится рюкзак и его хп в таблице user"""
    logging.info('delete_all_things_from_put_on_backpack')

    if pocket:
        pocket1 = await rq.get_Pocket1(tg_id)
        if pocket1:
            await rq.set_pocket1(tg_id, list(pocket1.keys())[0], 0)
        pocket2 = await rq.get_Pocket2(tg_id)
        if pocket2:
            await rq.set_pocket2(tg_id, list(pocket2.keys())[0], 0)

    backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
    if backpack_put_on == Backpack.backpack_foliage:
        cell1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        if cell1:
            await rq.set_b_foliage_cell_1(tg_id=tg_id, name_column=list(cell1.keys())[0], current_value=0)
        cell2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        if cell2:
            await rq.set_b_foliage_cell_2(tg_id=tg_id, name_column=list(cell2.keys())[0], current_value=0)
    elif backpack_put_on == Backpack.backpack_leana:
        cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        if cell1:
            await rq.set_b_leana_cell_1(tg_id=tg_id, name_column=list(cell1.keys())[0], current_value=0)
        cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        if cell2:
            await rq.set_b_leana_cell_2(tg_id=tg_id, name_column=list(cell2.keys())[0], current_value=0)
        cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        #logging.info(f'\ncell3 = {cell3}')
        if cell3:
            await rq.set_b_leana_cell_3(tg_id=tg_id, name_column=list(cell3.keys())[0], current_value=0)
        cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)
        if cell4:
            await rq.set_b_leana_cell_4(tg_id=tg_id, name_column=list(cell4.keys())[0], current_value=0)
    if del_backpack_xp:
        await rq.set_user(tg_id, "backpack", "no_backpack")
        await rq.set_user(tg_id, "xp_backpack", 0)



# возвращает True, если хр НАДЕТОГО рюкзака больше 0
async def check_xp_put_on_backpack_if_more_then_zero (tg_id: int) -> bool:
    """ возвращает True, если хр НАДЕТОГО рюкзака больше 0 """
    logging.info(f'check_xp_put_on_backpack_if_more_then_zero')

    backpack = await what_backpack_put_on(tg_id=tg_id) # какой рюкзак надет?
    #if '!' in data_backpack:
    #    backpack = data_backpack.split('!')[0] # в User[backpack] запись: 'no_backpack' или 'backpack_foliage!100'
    #else:
    #    backpack = data_backpack

    if backpack == Backpack.no_backpack:
        return False
    else:
        xp = (await rq.get_user_dict(tg_id=tg_id))['xp_backpack']
        logging.info(f'ХП РЮКЗАКА РАВНО = {xp}')

    if xp > 0:
        return True
    return False



# возвращает True, если вещи из рюкзака могут поместиться в карманы. Если True - перемещает в карманы, если False - перемещает в Хранилища
async def all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket(tg_id: int, clb: CallbackQuery | None=None) -> bool:
    """ возвращает True, если вещи из рюкзака могут быть перемещены в карманы. Если True - перемещает в карманы, если False (тут должна быть проверка на место локации)- перемещает в Хранилища"""

    logging.info('all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket')

    backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
    pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    pocket2 = await rq.get_Pocket2(tg_id=tg_id)
    common_dict: dict = {}

    if backpack_put_on == Backpack.backpack_foliage:
        cell1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        cell2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        cell3 = ''
        cell4 =''

    elif backpack_put_on == Backpack.backpack_leana:
        cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)
        common_dict: dict = {}
        dict_from_cell: dict = {}

    return_False = False
    if (cell1 and list(cell1.keys())[0] in LSWGC) or (cell2 and list(cell2.keys())[0] in LSWGC) or (cell3 and list(cell3.keys())[0] #LSWGC = list_storage_wardrobe_and_gun_and_craft
        in LSWGC) or (cell4 and list(cell4.keys())[0] in LSWGC): # если в ячейке рюкзака есть или броня. или оружие, то в карман не пойдет
        logging.info('ВРЕМЕННО 1--- all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket')
        return_False = True #дальше я проверю эту переменную. Если она существует, т.е. True, то значит я сюда провалился, вещи или оружие есть.
        # ВСЯ Функция вернет False -> и если location == landing_place => перемещать в Хранилища
        # а если return_False осталвсь False, то значит, что нет вещей из Wardrobe или Gun

    # составляем общий словарь со всеми вещами из карманов и всех ячеек
    if cell1:
        if list(cell1.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell1)
        else:
            key = list(cell1.keys())[0]
            if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                common_dict.update({key: f"{common_dict[key]}!{cell1[key]}"})
            else: # если вещь из трэша
                common_dict.update({key: common_dict[key]+cell1[key]})
        logging.info(f'if cell1 --- common_dict = {common_dict}')

    if cell2:
        if list(cell2.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell2)
        else:
            key = list(cell2.keys())[0]
            if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                common_dict.update({key: f"{common_dict[key]}!{cell2[key]}"})
            else: # если вещь из трэша
                common_dict.update({key: common_dict[key]+cell2[key]})
        logging.info(f'if cell2 --- common_dict = {common_dict}')

    if cell3:
        if list(cell3.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell3)
        else:
            key = list(cell3.keys())[0]
            if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                common_dict.update({key: f"{common_dict[key]}!{cell3[key]}"})
            else: # если вещь из трэша
                common_dict.update({key: common_dict[key]+cell3[key]})
        logging.info(f'if cell3 --- common_dict = {common_dict}')

    if cell4:
        if list(cell4.keys())[0] not in list(common_dict.keys()):
            common_dict.update(cell4)
        else:
            key = list(cell4.keys())[0]
            if key in LSWG: # Если вещь из брони / оружия, то добавляем проценты через !
                common_dict.update({key: f"{common_dict[key]}!{cell4[key]}"})
            else: # если вещь из трэша
                common_dict.update({key: common_dict[key]+cell4[key]})
        logging.info(f'if cell4 --- common_dict = {common_dict}')

    dict_from_cell = common_dict.copy()

    if pocket1:
        if list(pocket1.keys())[0] not in list(common_dict.keys()):
            common_dict.update(pocket1)
        else:
            key = list(pocket1.keys())[0]
            common_dict.update({key: common_dict[key]+pocket1[key]})

    if pocket2:
        if list(pocket2.keys())[0] not in list(common_dict.keys()):
            common_dict.update(pocket2)
        else:
            key = list(pocket2.keys())[0]
            common_dict.update({key: common_dict[key]+pocket2[key]})
    logging.info(f"ВРЕМЕННО СЛОВАРЬ == common_dict = {common_dict}")

    # также проверяем чему равно return_False. Если True? то есть броня / оружие
    # ЕСЛИ НЕ МОЖЕТ ВМЕСТИТЬСЯ В КАРМАНЫ
    if return_False or len(list(common_dict.keys()))>2 or (len(list(common_dict.keys()))==2 and (list(common_dict.values())[0]>20 or list(common_dict.values())[1]>=20)) or (len(list(common_dict.keys()))==1 and list(common_dict.values())[0]>40):
        logging.info('ВРЕМЕННО 2 ---- ЕСЛИ НЕ МОЖЕТ ВМЕСТИТЬСЯ В КАРМАНЫ также проверяем чему равно return_False. Если True? то есть броня / оружие')

        #  В ТЗ в шкаф перемещается если персонаж на локации 'Место посадки'
        # Если ДА, то перемещаем в шкафы
        data_user = await rq.get_user_dict(tg_id=tg_id)
        if data_user['location'] == 'landing_place':

            # проход по словарю из всех ячеек и распределение по шкафам
            for key, value in dict_from_cell.items():
                if key in LST:
                    value_in_starage = (await rq.get_StorageTrash(tg_id=tg_id))[key]
                    await rq.set_storage_trash(tg_id=tg_id, name_column=key, current_value=value_in_starage+value)
                elif key in LSW:
                    value_in_starage = (await rq.get_StorageWardrobe(tg_id=tg_id))[key]
                    if value_in_starage:
                        await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                    else:
                        await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=str(value))
                elif key in LSG:
                    value_in_starage = (await rq.get_StorageGun(tg_id=tg_id))[key]
                    if value_in_starage:
                        await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                    else:
                        await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=str(value))

            logging.info(f'ВРЕМЕННО 3 --- common_dict = {common_dict} --- dict_from_cell = {dict_from_cell}')

            return False

        else: # Локация НЕ 'Место посадки' УДАЛИТЬ ВСЕ ВЕЩИ ИЗ РЮКЗАКА И УДАЛИТЬ РЮКЗАК
            await delete_all_things_from_put_on_backpack(tg_id=tg_id, del_backpack_xp='del_backpack_xp')
            return False
        ### ЖДУ ответа
        #else:
         #   await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
          #  await clb.message.edit_caption(
           # caption=f'не вместиловь в новый рюкзак',
            #reply_markup=keyboard)


    logging.info('ВРЕМЕННО 4 --- Если я пришел сюда, то в карманы может быть перенесено, то, что есть в рюкзаке Значит, делаю этот перенос')

    # Если я пришел сюда, то в карманы может быть перенесено, то, что есть в рюкзаке
    # Значит, делаю этот перенос
    logging.info(f'ВРЕМЕННО 5 --- common_dict = {common_dict} --- dict_from_cell = {dict_from_cell}')

    # перед установкой новых значений зануляем все ячейки в Pocket, а рюкзак и так удолиться
    await delete_all_things_from_put_on_backpack(tg_id=tg_id, pocket='pocket')
    if len(common_dict) == 2: # если в словаре два ключа, то первый в карман 1, второй в крман 2
        key1 = list(common_dict.keys())[0]
        key2 = list(common_dict.keys())[1]
        await rq.set_pocket1(tg_id=tg_id, name_column=key1, current_value=common_dict[key1])
        await rq.set_pocket2(tg_id=tg_id, name_column=key2, current_value=common_dict[key2])
    elif len(common_dict) == 1: # если в словаре один ключ, и если <= 20, то в 1 карман, если > 20? то сперва 20 в карман 1, остальное в карман 2
        key = list(common_dict.keys())[0]
        if common_dict[key] <=20:
            await rq.set_pocket1(tg_id=tg_id, name_column=key, current_value=common_dict[key])
        else:
            await rq.set_pocket1(tg_id=tg_id, name_column=key, current_value=20)
            await rq.set_pocket2(tg_id=tg_id, name_column=key, current_value=common_dict[key]-20)


    return True



# если ХП рюкзака = 0, то запускаю эту функцию
async def xp_backpack_is_over_remove_things_delate_backpack(clb: CallbackQuery, tg_id: str, backpack: str) -> None:
    """ если ХП рюкзака = 0, то запускаю эту функцию"""
    logging.info('xp_backpack_is_over_remove_things_delate_backpack')
    keyboard = kb.create_in_kb(1, **{'ok': 'backpack'})

    # первый вопрос: ВСЁ может вместиться в пустые карманы?

    # если может вместиться, перемещаем в карманы
    # НО, проверка на локацию, и если "Место посадки", то перенос в Хранилища
    if await all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket(tg_id=tg_id):
        logging.info('xp_backpack_is_over_remove_things_delate_backpack --- if all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket(tg_id=tg_id):')

        await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
        await clb.message.edit_caption(caption=f"{LSW[backpack]} сломался. \n Всё перенесено в карманы", reply_markup=keyboard)

        # перенос из рюкзака в карманы реализован в функции all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket
        await delete_all_things_from_put_on_backpack(tg_id=tg_id)
        await rq.set_user(tg_id=tg_id, name_column='backpack', current_value='no_backpack')# устанавливаем в User no_backpack
        await clb.answer()
    else: # НЕ может переместиться в карманы. Если landing_place, то перенос в Хранилища, если другая локация, то ### СДЕЛАЙ НОВЫЙ БЛОК (как и внизу справа)
        # перенос из рюкзака в ХРАНИЛИЩА реализован в функции all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket

        logging.info('xp_backpack_is_over_remove_things_delate_backpack --- ELSE --- NOT all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket(tg_id=tg_id):')
        location = (await rq.get_user_dict(tg_id=tg_id))['location']
        if location == Location.landing_place:
            logging.info('xp_backpack_is_over_remove_things_delate_backpack --- ELSE --- NOT all_things_can_be.....  if location == Location.landing_place:')

            dict_with_all_things_in_ = await dict_with_all_things_from_backpack(tg_id=tg_id)
            logging.info(f'xp_backpack_is_over_remove_things_delate_backpack --- ELSE --- NOT all_things_can_be..... dict_with_all_things_in_backpack = {dict_with_all_things_in_}')

            str_to_capture = await modify_dict_with_all_things_from_backpack_to_srt_with_enter(dict_=dict_with_all_things_in_)
            logging.info(f'xp_backpack_is_over_remove_things_delate_backpack --- ELSE --- NOT all_things_can_be..... str_to_capture = {str_to_capture}')

            await delete_all_things_from_put_on_backpack(tg_id=tg_id, del_backpack_xp='del_backpack_xp')
            await rq.set_user(tg_id=tg_id, name_column='backpack', current_value='no_backpack')# устанавливаем в User no_backpack
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N38']))
            await clb.message.edit_caption(caption=f"{LSW[backpack]} сломался \nи было перенесено в Хранилище:\n{str_to_capture}"
                                                   , reply_markup=keyboard)

            await clb.answer()
        else:
            await clb.message.edit_media(media=InputMediaPhoto(media=ph['N17']))
            await clb.message.edit_caption(caption=f"{LSW[backpack]} сломался \nвещи выброшены."
                                                   , reply_markup=keyboard)


# Возвращает список списков для клавиатуры с цветными кнопками
# при взаимодействии рюкзака с любыми Хранилищами. ЕСТЬ желтые ячейки.
async def create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell(
        tg_id: int,
        value_pocket_cell: int,
        #value_storage: int,
        prefix: str = 'X',

        backpack: str = 'X' ,
        clb_pocket_cell: str = 'X' ,
        clb_name: str = 'X' ,
        clb_back: str = 'X',) -> list:
    """
    Возвращает список списков для клавиатуры с цветными кнопками,
    при взаимодействии рюкзака с любыми Хранилищами. ЕСТЬ желтые ячейки.
    """
    logging.info(f"create_list_for_create_keyboard_to_backpack_with_colored_cell_with_yellow_cell")
    list_pocket: list = []
    list_cell: list = []
    green = '🟩'
    yellow = '🟨'
    red = '🟥'
    #backpack = await what_backpack_put_on(tg_id=tg_id) # на ! проверка есть

    dict_pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    dict_pocket2 = await rq.get_Pocket2(tg_id=tg_id)
    logging.info(f'dict_pocket1 = {dict_pocket1} --- dict_pocket2 = {dict_pocket2}')

                                        #list_storage_trash_drag as lstd,
    if not dict_pocket1 and clb_name in lstd: # одинарная проверка: только словарь с вещами должен быть пустой
            list_pocket.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket1'}"])
    elif dict_pocket1 and clb_name in lstd and clb_name in dict_pocket1 and dict_pocket1[clb_name]<20 and clb_pocket_cell != 'pocket1':
            list_pocket.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket1'}"])
    else:
            list_pocket.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket1'}"])

    if not dict_pocket2 and clb_name in lstd: # одинарная проверка: только словарь с вещами должен быть пустой
            list_pocket.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket2'}"])
    elif dict_pocket2 and clb_name in lstd and clb_name in dict_pocket2 and dict_pocket2[clb_name]<20 and clb_pocket_cell != 'pocket2':
            list_pocket.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket2'}"])
    else:
            list_pocket.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'pocket2'}"])


    if backpack == Backpack.no_backpack: # взаимодействие тоьлко с карманами
        logging.info(f"ВРЕМЕННО 911 --- list_pocket = {list_pocket}")
        return list_pocket

    elif backpack == Backpack.backpack_foliage:

        dict_cell_1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        dict_cell_2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        logging.info(f"ВРЕМЕННО 918 --- dict_cell_1 = {dict_cell_1} --- dict_cell_2 = {dict_cell_2}")

        if not dict_cell_1: # одинарная проверка: только словарь с вещами должен быть пустой
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])
        # словарь не пустой, вещь в новой ячейке, куда хотят положить такая же, этой вещи не более 20 штук и это не "своя же" ячейка
        elif dict_cell_1 and clb_name in dict_cell_1 and list(dict_cell_1)[0] not in LSWG and dict_cell_1[clb_name]<20 and clb_pocket_cell != 'cell_1':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])
        else:
            list_cell.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])

        if not dict_cell_2:
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])
        elif dict_cell_2 and clb_name in dict_cell_2 and list(dict_cell_2)[0] not in LSWG and dict_cell_2[clb_name]<20 and clb_pocket_cell != 'cell_2':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])
        else:
            list_cell.append([red, f"{prefix}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])


    elif backpack == Backpack.backpack_leana:

        dict_cell_1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        dict_cell_2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        dict_cell_3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        dict_cell_4 = await rq.get_BLeanaCell_4(tg_id=tg_id)


        if not dict_cell_1: # одинарная проверка: только словарь с вещами должен быть пустой
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])
        elif dict_cell_1 and clb_name in dict_cell_1 and list(dict_cell_1)[0] not in LSWG and (list(dict_cell_1)[0] not in LSWG and dict_cell_1[clb_name]<20) and clb_pocket_cell != 'cell_1':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])
        else:
            list_cell.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_1'}"])

        if not dict_cell_2:
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])
        elif dict_cell_2 and clb_name in dict_cell_2 and list(dict_cell_2)[0] not in LSWG and (list(dict_cell_2)[0] not in LSWG and dict_cell_2[clb_name]<20) and clb_pocket_cell != 'cell_2':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])
        else:
            list_cell.append([red, f"{prefix}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_2'}"])

        if not dict_cell_3:
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_3'}"])
        elif dict_cell_3 and clb_name in dict_cell_3 and list(dict_cell_3)[0] not in LSWG and (list(dict_cell_3)[0] not in LSWG and dict_cell_3[clb_name]<20) and clb_pocket_cell != 'cell_3':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_3'}"])
        else:
            list_cell.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_3'}"])

        if not dict_cell_4:
            list_cell.append([green, f"{prefix}!{clb_name}!{backpack}!{'g'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_4'}"])
        elif dict_cell_4 and clb_name in dict_cell_4 and list(dict_cell_4)[0] not in LSWG and (list(dict_cell_4)[0] not in LSWG and dict_cell_4[clb_name]<20) and clb_pocket_cell != 'cell_4':
            list_cell.append([yellow, f"{prefix}!{clb_name}!{backpack}!{'y'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_4'}"])
        else:
            list_cell.append([red, f"{prefix}!{clb_name}!{backpack}!{'r'}!{clb_pocket_cell}!{value_pocket_cell}!{'cell_4'}"])

        logging.info(f"ВРЕМЕННО 972 --- list_pocket = {list_pocket} --- list_cell = {list_cell}")
    logging.info(f"ВРЕМЕННО 973 перед return --- list_pocket = {list_pocket} --- list_cell = {list_cell}")
    return (list_pocket, list_cell)



# устанавливает нужное значение в нужную колонку нужного ячейки / кармана нужного рюкзака
async def set_value_in_pocket_cell_put_on_backpack(
        tg_id:int,
        pocket_cell: str,
        clb_name:str,
        value: int,
        backpack: str|None=None,
) -> None:
    """устанавливает нужное значение в нужную колонку нужного ячейки / кармана нужного рюкзака"""

    logging.info('set_value_in_pocket_cell_put_on_backpack')

    if pocket_cell == 'pocket1':
            await rq.set_pocket1(tg_id=tg_id, name_column=clb_name, current_value=value)
    elif pocket_cell == 'pocket2':
        await rq.set_pocket2(tg_id=tg_id, name_column=clb_name, current_value=value)

    if backpack == Backpack.backpack_foliage and pocket_cell.startswith('cell'): # чтобы не заходило сюда, если в карманы зашло
        if pocket_cell == 'cell_1':
            await rq.set_b_foliage_cell_1(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_2':
            await rq.set_b_foliage_cell_2(tg_id=tg_id, name_column=clb_name, current_value=value)

    elif backpack == Backpack.backpack_leana and pocket_cell.startswith('cell'): # чтобы не заходило сюда, если в карманы зашло
        if pocket_cell == 'cell_1':
            await rq.set_b_leana_cell_1(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_2':
            await rq.set_b_leana_cell_2(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_3':
            await rq.set_b_leana_cell_3(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_4':
            await rq.set_b_leana_cell_4(tg_id=tg_id, name_column=clb_name, current_value=value)


# Переносит вещи из карманов и рюкзака в хранилище
# И МОЖЕТ БЫТЬ ОБРАТНО
# И МОЖЕТ БЫТЬ УДАЛЯЕТ, ДОКЛАДЫВАЕТ, ПЕРЕКЛЫДЫВАЕТ
async def move_select_thing_backpack_storage(
        tg_id: int | None=None,
        value_pocket_cell: int | None=None, # сколько вещей находится в кармане / ячейке
        button_value: int | None=None,
        #value_storage: int,
        clb_action: str = ' ',
        prefix: str = ' ',
        backpack: str = ' ' ,
        pocket_cell: str = ' ' ,
        clb_name: str = ' ' ,
        clb_back: str = ' '
) -> int | None:
    """Переносит вещи из карманов и рюкзака в хранилище"""

    logging.info(f"move_select_thing_backpack_storage --- button_value = {button_value}")

    # b4!1!put_in_storage!backpack_leana!pocket2!bandages!6

    if clb_action == 'put_in_storage':
        if button_value == 777: # до полного
            button_value = 20 - value_pocket_cell
        elif button_value == 333: # все
            button_value = value_pocket_cell
        elif clb_name in LSWG: # если броня / оружие, то тогда проценты
            button_value = value_pocket_cell

        value = value_pocket_cell-button_value
        logging.info(f"ВРЕМЕННО 794 value={value}")


    elif clb_action == 'dologit':
        #logging.info(f"ВРЕМЕННО 798 button_value = {button_value} --- value_pocket_cell={value_pocket_cell} --- ")
        if button_value == 777: # до полного
            button_value = 20 - value_pocket_cell
            #logging.info(f"ВРЕМЕННО 801 button_value = {button_value} --- value_pocket_cell={value_pocket_cell} --- ")
        elif button_value == 333: # все
            button_value = (await rq.get_StorageTrash(tg_id=tg_id))[clb_name]
            #logging.info(f"ВРЕМЕННО 804 button_value = {button_value} --- value_pocket_cell={value_pocket_cell} ---")
        elif clb_name in LSWG: # если броня / оружие, то тогда проценты
            button_value = value_pocket_cell
        value = value_pocket_cell+button_value
        logging.info(f"ВРЕМЕННО 808 button_value = {button_value} --- value_pocket_cell={value_pocket_cell} --- value={value}")


    # старое значение в рюкзаке = value_pocket_cell
    # новое значение в рюкзаке = value_pocket_cell - button_value
    if pocket_cell == 'pocket1':
        await rq.set_pocket1(tg_id=tg_id, name_column=clb_name, current_value=value)
    elif pocket_cell == 'pocket2':
        await rq.set_pocket2(tg_id=tg_id, name_column=clb_name, current_value=value)

    if backpack == Backpack.backpack_foliage and pocket_cell.startswith('cell'): # чтобы не заходило сюда, если в карманы зашло
        if pocket_cell == 'cell_1':
            await rq.set_b_foliage_cell_1(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_2':
            await rq.set_b_foliage_cell_2(tg_id=tg_id, name_column=clb_name, current_value=value)

    elif backpack == Backpack.backpack_leana and pocket_cell.startswith('cell'): # чтобы не заходило сюда, если в карманы зашло
        if pocket_cell == 'cell_1':
            await rq.set_b_leana_cell_1(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_2':
            await rq.set_b_leana_cell_2(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_3':
            await rq.set_b_leana_cell_3(tg_id=tg_id, name_column=clb_name, current_value=value)
        elif pocket_cell == 'cell_4':
            await rq.set_b_leana_cell_4(tg_id=tg_id, name_column=clb_name, current_value=value)

    # старое значение в хранилище - через value_storage=rq.get
    # новое значение в рюкзаке = value_storage + button_value
    if clb_name in LST and clb_action == 'put_in_storage':
        # cvs = current_value_storage
        cvs = (await rq.get_StorageTrash(tg_id=tg_id))[clb_name]
        await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=cvs+button_value)
    elif clb_name in LST and clb_action == 'dologit':
        # cvs = current_value_storage
        cvs = (await rq.get_StorageTrash(tg_id=tg_id))[clb_name]
        await rq.set_storage_trash(tg_id=tg_id, name_column=clb_name, current_value=cvs-button_value)
        value_storage_dologit = button_value
        return value_storage_dologit
    elif clb_name in LSW:
        cvs = (await rq.get_StorageWardrobe(tg_id=tg_id))[clb_name]
        await rq.set_storage_wardrobe(tg_id=tg_id, name_column=clb_name, current_value=f"{cvs}!{button_value}")
    elif clb_name in LSG:
        cvs = (await rq.get_StorageGun(tg_id=tg_id))[clb_name]
        await rq.set_storage_gun(tg_id=tg_id, name_column=clb_name, current_value=f"{cvs}!{button_value}")


# возвращает значение из той вещи, которая лежит в ячейке / кармане надетого рюкзака
async def what_thing_value_in_the_pocket_cell_put_on_backpack(
        tg_id:int,
        pocket_cell: str,
        backpack: str|None=None
) -> list:
    """возвращает список 1 элемент = название вещи 2 элемент = количество/проценты той вещи,
    которая лежит в ВХОД. ДАН.ячейке/кармане надетого рюкзака, чтобы из ячейки рюкзака получить, надо передать 'backpack'"""

    logging.info('what_thing_value_in_the_pocket_cell_put_on_backpack')


    if pocket_cell == 'pocket1':
        dict_ = await rq.get_Pocket1(tg_id=tg_id)
    elif pocket_cell == 'pocket2':
        dict_ = await rq.get_Pocket2(tg_id=tg_id)

    if backpack:
        if backpack == "backpack_foliage":
            if pocket_cell == "cell_1":
                dict_ = await rq.get_BFoliageCell_1(tg_id=tg_id)
            elif pocket_cell == "cell_2":
                dict_ = await rq.get_BFoliageCell_2(tg_id=tg_id)

        if backpack == "backpack_leana":
            if pocket_cell == "cell_1":
                dict_ = await rq.get_BLeanaCell_1(tg_id=tg_id)
            elif pocket_cell == "cell_2":
                dict_ = await rq.get_BLeanaCell_2(tg_id=tg_id)
            elif pocket_cell == "cell_3":
                dict_ = await rq.get_BLeanaCell_3(tg_id=tg_id)
            elif pocket_cell == "cell_4":
                dict_ = await rq.get_BLeanaCell_4(tg_id=tg_id)
    #logging.info(f" --- dict_ = {dict_ if dict_ else None} {True if dict_ else False}")
    if dict_:
        key=(list(dict_))[0]
        value = dict_[key]
        #logging.info(f"key = {key} --- value = {value}")
        return [key, value]
    return [None, 0]



# Снимает надетую броню или оружие и переносит или в рюкзак, или в Хранилище
async def put_off_armor_or_gun_and_take_this_on_wardrobe_or_backpack(
        tg_id: int,
        armor_or_gun: str, #backpack_foliage, helmet_kosmonavt, G17, spear
        wardrobe_or_backpack: str,
        cell: str | None=None,
        hand: str | None=None
) -> str: # new_percent
    """Снимает надетую броню или оружие и переносит или в рюкзак, или в Хранилище, возвращает новые проценты, переведенные из ХП"""

    logging.info('put_off_armor_or_gun_and_take_this_on_wardrobe_or_backpack')

    data_user = await rq.get_user_dict(tg_id=tg_id)

    if '_' in armor_or_gun: # если '_' есть, то вещь - не оружие
        name_column_User = armor_or_gun.split('_')[0]
        thing_percent = data_user[name_column_User]
    else: # а если оружие, то name_column_User это какая-то рука
        name_column_User = hand # пришло на вход функции
        thing_percent = data_user[name_column_User]
    logging.info(f'name_column_User = {name_column_User} --- armor_or_gun = {armor_or_gun} --- thing_percent = {thing_percent}')

    if '!' in thing_percent: # мы пытаемся проценты в таблице user актуализировать с ХП вещи, на здесь все равно делать перевод в проценты из ХП
        percent = thing_percent.split('!')[-1]

    xp = data_user[f'xp_{name_column_User}']
    new_percent = (100 * xp) / dict_percent_xp[armor_or_gun]
    if new_percent >= 1:
        new_percent = str(round(new_percent))
    else:
        new_percent = str(int(new_percent))

    logging.info(f'name_column_User = {name_column_User} --- armor_or_gun = {armor_or_gun} --- thing_percent = {thing_percent} --- new_percent = {new_percent} ---- xp = {xp}')

    # перебор всех колонок и реализация функции
    # сперва шкаф
    if wardrobe_or_backpack == 'wardrobe':
        if name_column_User in ['backpack', 'helmet', 'dress', 'shoes']:
            if name_column_User != 'backpack': # для 'helmet', 'dress', 'shoes' пустые '' ячейки
                # установка пустой строки в таблице User в названии вещи
                await rq.set_user(tg_id=tg_id, name_column=name_column_User, current_value='')
            else: # для рюкзака 'no_backpack'
                await rq.set_user(tg_id=tg_id, name_column=name_column_User, current_value='no_backpack')
            # установка 0 в таблице User в XP_названии вещи
            await rq.set_user(tg_id, f'xp_{name_column_User}', 0)

            data_ = await rq.get_StorageWardrobe(tg_id=tg_id)
            new_value = data_[armor_or_gun]+'!'+new_percent
            await rq.set_storage_wardrobe(tg_id, armor_or_gun, new_value)

        elif name_column_User in ['left_hand', 'right_hand']:
            await rq.set_user(tg_id=tg_id, name_column=name_column_User, current_value='')
            # установка 0 в таблице User в XP_названии вещи
            await rq.set_user(tg_id, f'xp_{name_column_User}', 0)
            data_ = await rq.get_StorageGun(tg_id=tg_id)
            new_value = str(data_[armor_or_gun])+'!'+new_percent
            await rq.set_storage_gun(tg_id, armor_or_gun, new_value)

    elif wardrobe_or_backpack == 'backpack': # если положить надо в рюкзак
        backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
        await set_value_in_pocket_cell_put_on_backpack(
            tg_id=tg_id,
            backpack=backpack_put_on,
            pocket_cell=cell,
            clb_name=armor_or_gun,
            value=new_percent
        )

    return new_percent
#        if backpack_put_on == Backpack.backpack_foliage:
#            if cell == 'cell_1':
#                await rq.set_backpack_foliage(tg_id, armor_or_gun, 20)
#            elif cell == 'cell_2':
#                await rq.set_backpack_foliage(tg_id, armor_or_gun, 20)
#        elif backpack_put_on == Backpack.backpack_leana:
#            if cell == 'cell_1':
#                await rq.set_backpack_leana(tg_id, armor_or_gun, 20)
#            elif cell == 'cell_2':
#                await rq.set_backpack_leana(tg_id, armor_or_gun, 20)
#            elif cell == 'cell_3':
#                await rq.set_backpack_leana(tg_id, armor_or_gun, 20)
#            elif cell == 'cell_4':
#                await rq.set_backpack_leana(tg_id, armor_or_gun, 20)




# # ДЕЙСТВИЯ
# 1 Забиваем новый рюкзак как можем
# 2 Оставшиеся вещи перемещаем в соответствующие хранилища и информируем об этих вещах игрока,
# 3 надеваем новый рюкзак,
# 4 старый кладем в шкаф
# 5 кнопка ок премещает в checking_where_avatar_is_located
async def things_put_on_in_backpack_foliage_after_put_on_in_storages(tg_id: int, percent_backpack_foliage: str) -> list[str, dict]:
    """ # 1 Забиваем новый рюкзак как можем
        #    Если локация landing_place то
        # 2 Оставшиеся вещи перемещаем в соответствующие хранилища и информируем об этих вещах игрока,
            Если локация НЕ landing_place то оставшиеся вещи помещаем в словарь и высвечиваем на клавиатере (с вещами работаем дальше)
        # 3 надеваем новый рюкзак,
        # 4 старый кладем в шкаф
        # 5 кнопка ок премещает в checking_where_avatar_is_located"""

    logging.info('all_things_can_be_moved_from_backpack_with_zero_xp_to_pocket')
    location = (await rq.get_user_dict(tg_id))['location']

    #backpack_put_on = await what_backpack_put_on(tg_id=tg_id)
    #pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    #pocket2 = await rq.get_Pocket2(tg_id=tg_id)
   # common_dict: dict = {}

    #if backpack_put_on == Backpack.backpack_foliage:
     #   cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
      #  cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)

    #elif backpack_put_on == Backpack.backpack_leana:
    cell1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
    cell2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
    cell3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
    cell4 = await rq.get_BLeanaCell_4(tg_id=tg_id)


    if cell1: # если в ячейке 1 что-то есть
        await set_value_in_pocket_cell_put_on_backpack(tg_id=tg_id, backpack='backpack_foliage', pocket_cell='cell_1', clb_name=list(cell1.keys())[0], value=list(cell1.values())[0])
        if cell2: # если при этом в ячейке 2 тоже что-то есть
            await set_value_in_pocket_cell_put_on_backpack(tg_id=tg_id, backpack='backpack_foliage', pocket_cell='cell_2', clb_name=list(cell2.keys())[0], value=list(cell2.values())[0])
        else:
            await set_value_in_pocket_cell_put_on_backpack(tg_id=tg_id, backpack='backpack_foliage', pocket_cell='cell_2', clb_name=list(cell3.keys())[0], value=list(cell3.values())[0])
    elif cell2: # если в ячейке 1 ничего нет: заносим в новый рюкзак из 2 и 3 ячейки, а следующую пропускаем
        await set_value_in_pocket_cell_put_on_backpack(tg_id=tg_id, backpack='backpack_foliage', pocket_cell='cell_1', clb_name=list(cell2.keys())[0], value=list(cell2.values())[0])
        await set_value_in_pocket_cell_put_on_backpack(tg_id=tg_id, backpack='backpack_foliage', pocket_cell='cell_2', clb_name=list(cell3.keys())[0], value=list(cell3.values())[0])


    str_return: str = ''
    dict_return: dict = {}

    if cell3 and (cell1 and cell2):
        key = list(cell3.keys())[0]
        value = list(cell3.values())[0]
        if location == Location.landing_place:
            if key in LST:
                value_in_starage = (await rq.get_StorageTrash(tg_id=tg_id))[key]
                await rq.set_storage_trash(tg_id=tg_id, name_column=key, current_value=value_in_starage+value)
            elif key in LSW:
                value_in_starage = (await rq.get_StorageWardrobe(tg_id=tg_id))[key]
                if value_in_starage:
                    await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                else:
                    await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=str(value))

            elif key in LSG:
                value_in_starage = (await rq.get_StorageGun(tg_id=tg_id))[key]
                if value_in_starage:
                    await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                else:
                    await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=str(value))
        str_return = f"{All_Th[key]} {value}\n"
        dict_return[key] = value

    if cell4:
        key = list(cell4.keys())[0]
        value = list(cell4.values())[0]
        if location == Location.landing_place:
            if key in LST:
                value_in_starage = (await rq.get_StorageTrash(tg_id=tg_id))[key]
                await rq.set_storage_trash(tg_id=tg_id, name_column=key, current_value=value_in_starage+value)
            elif key in LSW:
                value_in_starage = (await rq.get_StorageWardrobe(tg_id=tg_id))[key]
                if value_in_starage:
                    await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                else:
                    await rq.set_storage_wardrobe(tg_id=tg_id, name_column=key, current_value=str(value))

            elif key in LSG:
                value_in_starage = (await rq.get_StorageGun(tg_id=tg_id))[key]
                if value_in_starage:
                    await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=f"{value_in_starage}!{value}")
                else:
                    await rq.set_storage_gun(tg_id=tg_id, name_column=key, current_value=str(value))
        str_return += f"{All_Th[key]} {value}"
        dict_return[key] = value
    #if (await rq.get_user_dict(tg_id)['location'])!='landing_place':
    #    return str_return

    # снимаем рюкзак и кладем в шкаф
    backpack = (await rq.get_StorageWardrobe(tg_id))[Backpack.backpack_leana]
    data_user_backpack = (await rq.get_user_dict(tg_id))['backpack'].split('!')[-1]
    if backpack:
        await rq.set_storage_wardrobe(tg_id, Backpack.backpack_leana, backpack+'!'+data_user_backpack)### перевод хп в проценты из state, а пока % из user
    else:
        await rq.set_storage_wardrobe(tg_id, Backpack.backpack_leana, data_user_backpack)

    # Зануляем все ячейки в надетом (леанном) рюкзаке
    await delete_all_things_from_put_on_backpack(tg_id)

    # убираем из шкафа надетый рюкзак
    str_backpack_foliage = (await rq.get_StorageWardrobe(tg_id))[Backpack.backpack_foliage]
    new_str_backpack = await modify_str_to_str_del_choise_percent_and_null(str_backpack_foliage, percent_backpack_foliage)
    await rq.set_storage_wardrobe(tg_id, 'backpack_foliage', new_str_backpack)

    logging.info(f'ВРЕМЕННО 1088 --- cell1 = {cell1} --- cell2 = {cell2} --- cell3 = {cell3} --- cell4 = {cell4} --- str_return = {str_return} --- backpack = {backpack} --- dict_return = {dict_return}')
    return [str_return, dict_return]



# На вход подается словарь с вещами и название рюкзака. Вещи из словаря кладутся в этот рюкзак
async def put_in_backpack_things_from_dict(tg_id: int, dict_things: dict, backpack: str) -> None:
    """ На вход подается словарь с вещами и название рюкзака. Вещи из словаря кладутся в этот рюкзак"""

    logging.info('put_in_backpack_things_from_dict')
    if len(dict_things)>2:
        logging.info(f'put_in_backpack_things_from_dict --- ДЛИНА СЛОВАРЯ = {len(dict_things)}')
        return

    for key, value in dict_things.items():
        if backpack == Backpack.backpack_foliage:
            cell_1 = await rq.get_BFoliageCell_1(tg_id)
            cell_2 = await rq.get_BFoliageCell_2(tg_id)
            if '!' not in str(value):
                if not cell_1:
                    await rq.set_b_foliage_cell_1(tg_id, key, int(value))
                else:
                    await rq.set_b_foliage_cell_2(tg_id, key, int(value))
            else:
                list_value = value.split('!')
                await rq.set_b_foliage_cell_1(tg_id, key, int(list_value[0]))
                await rq.set_b_foliage_cell_2(tg_id, key, int(list_value[1]))

        elif backpack == Backpack.backpack_leana:
            cell_1 = await rq.get_BLeanaCell_1(tg_id)
            if '!' not in str(value):
                if not cell_1:
                    await rq.set_b_leana_cell_1(tg_id, key, int(value))
                else:
                    await rq.set_b_leana_cell_2(tg_id, key, int(value))
            else:
                list_value = value.split('!')
                await rq.set_b_leana_cell_1(tg_id, key, int(list_value[0]))
                await rq.set_b_leana_cell_2(tg_id, key, int(list_value[1]))



# восстанавливает ХП игрока. вычитает 1 единицу лекарства из того места откуда взяли его
async def recover_xp_subtracts_drug(tg_id: int, pocket_cell: str, name_drug: str, value_drug: int|str, backpack: str|None=None) -> list:
    """ восстанавливает ХП игрока. вычитает 1 единицу лекарства из того места откуда взяли его"""

    logging.info('recover_xp_subtracts_drug')
    value_xp = (await rq.get_user_dict(tg_id=tg_id))['xp']

    if value_xp < 100 - int(dict_u[name_drug]):
        value_xp+=int(dict_u[name_drug])
    else:
        value_xp = 100

    await rq.set_user_xp(tg_id=tg_id, current_xp=value_xp)

    await set_value_in_pocket_cell_put_on_backpack(
        tg_id=tg_id, backpack=backpack,
        pocket_cell=pocket_cell,
        clb_name=name_drug,
        value=int(value_drug)-1
    )
    flag = True
    quantity_drugs = await what_thing_value_in_the_pocket_cell_put_on_backpack(tg_id, pocket_cell)
    if quantity_drugs[-1] < 1:
        flag = False

    return [value_xp, flag]



# dict_armor = {'helmet_kosmonavt': ['Шлем космонавта - Стандартный шлем космонавта.\nГрамостки,тяжелый и неудобный.', 5, 35, 45, 5000],
# рассчет урона броне, уменьшение хп и процентовки этой брони (на вход список [шлем, костюм, обувь])
async def armor_damage_subtracts_xp_percent(tg_id: int, list_demage: list, list_armor:list|None=None) -> list:
    """рассчет урона броне, уменьшение хп и процентовки этой брони (на вход список [шлем, костюм, обувь])"""

    logging.info(f'armor_damage_subtracts_xp_percent ----- list_demage = {list_demage}')

    data_user = await rq.get_user_dict(tg_id=tg_id)

    if data_user['helmet']:# если на игрока надет шлем
        helmet = data_user['helmet'].split('!')[0] # название надетого шлема из БД
        xp_helmet = data_user['xp_helmet'] # актуальное ХП из БД
        percent_helmet = xp_helmet*100/dict_armor[helmet][4] # и соответствующие ему %

        helmet_b = dict_armor[helmet][1]/100*percent_helmet  # 5/100*5 = 0.25 (0%)    | 5/100*95 = 4.75 (5%)
        helmet_x = dict_armor[helmet][2]/100*percent_helmet  # 35/100*5 = 1.75 (2%)   | 35/100*95 = 33.25 (33%)
        helmet_e = dict_armor[helmet][3]/100*percent_helmet  # 45/100*5 = 2.25 (2%)   | 35/100*95 = 42.75 (43%)
        helmet_b = round(helmet_b) if helmet_b>1 else int(helmet_b)
        helmet_x = round(helmet_x) if helmet_x>1 else int(helmet_x)
        helmet_e = round(helmet_e) if helmet_e>1 else int(helmet_e)

        demage = list_demage[0]-(list_demage[0]/100*helmet_b) + list_demage[1]-(list_demage[1]/100*helmet_x) + list_demage[2]-(list_demage[2]/100*helmet_e)
        demage = round(demage) if demage>1 else int(demage)
        new_xp_helmet = xp_helmet-demage

        if new_xp_helmet > 0:
            new_percent_helmet = new_xp_helmet*100/dict_armor[helmet][4]
            new_percent_helmet = round(new_percent_helmet) if new_percent_helmet>1 else int(new_percent_helmet)
            logging.info(f'\nlist_demage = {list_demage}\nhelmet_b = {helmet_b}\nhelmet_x = {helmet_x}\nhelmet_e = {helmet_e}\ndemage = {demage}\nnew_xp_helmet = {new_xp_helmet}\nnew_percent_helmet = {new_percent_helmet}')
            if new_percent_helmet > 0:
                await rq.set_user(tg_id=tg_id, name_column='helmet', current_value=f'{helmet}!{new_percent_helmet}')
                await rq.set_user(tg_id=tg_id, name_column='xp_helmet', current_value=new_xp_helmet)
                return [demage, helmet, new_percent_helmet]
            else:
                await rq.set_user(tg_id=tg_id, name_column='helmet', current_value='')
                return [demage, helmet, 0] # Если 3 элемент = 0, то эта броня уничтожена

    if data_user['dress']:
        dress = data_user['dress'].split('!')[0]
        xp_dress = data_user['xp_dress']
        percent_dress = xp_dress*100/dict_armor[dress][4]

        dress_b = dict_armor[dress][1]/100*percent_dress  # 5/100*5 = 0.25 (0%)    | 5/100*95 = 4.75 (5%)
        dress_x = dict_armor[dress][2]/100*percent_dress  # 35/100*5 = 1.75 (2%)   | 35/100*95 = 33.25 (33%)
        dress_e = dict_armor[dress][3]/100*percent_dress  # 45/100*5 = 2.25 (2%)   | 35/100*95 = 42.75 (43%)
        dress_b = round(dress_b) if dress_b>1 else int(dress_b)
        dress_x = round(dress_x) if dress_x>1 else int(dress_x)
        dress_e = round(dress_e) if dress_e>1 else int(dress_e)

        demage = list_demage[0]-(list_demage[0]/100*dress_b) + list_demage[1]-(list_demage[1]/100*dress_x) + list_demage[2]-(list_demage[2]/100*dress_e)
        demage = round(demage) if demage>1 else int(demage)
        new_xp_dress = xp_dress-demage
        if new_xp_dress > 0:
            new_percent_dress = new_xp_dress*100/dict_armor[dress][4]
            new_percent_dress = round(new_percent_dress) if new_percent_dress>1 else int(new_percent_dress)
            logging.info(f'\nlist_demage = {list_demage}\ndress_b = {dress_b}\ndress_x = {dress_x}\ndress_e = {dress_e}\ndemage = {demage}\nnew_xp_dress = {new_xp_dress}\nnew_percent_dress = {new_percent_dress}')
            if new_percent_dress > 0:
                await rq.set_user(tg_id=tg_id, name_column='dress', current_value=f'{dress}!{new_percent_dress}')
                await rq.set_user(tg_id=tg_id, name_column='xp_dress', current_value=new_xp_dress)
                return [demage, dress, new_percent_dress]
            else:
                await rq.set_user(tg_id=tg_id, name_column='dress', current_value='')
                return [demage, dress, 0] # Если 3-й элемент 0, то эта броня уничтожена


    if data_user['shoes']:
        shoes = data_user['shoes'].split('!')[0]
        xp_shoes = data_user['xp_shoes']
        percent_shoes = xp_shoes*100/dict_armor[shoes][4]

        shoes_b = dict_armor[shoes][1]/100*percent_shoes  # 5/100*5 = 0.25 (0%)    | 5/100*95 = 4.75 (5%)
        shoes_x = dict_armor[shoes][2]/100*percent_shoes  # 35/100*5 = 1.75 (2%)   | 35/100*95 = 33.25 (33%)
        shoes_e = dict_armor[shoes][3]/100*percent_shoes  # 45/100*5 = 2.25 (2%)   | 35/100*95 = 42.75 (43%)
        shoes_b = round(shoes_b) if shoes_b>1 else int(shoes_b)
        shoes_x = round(shoes_x) if shoes_x>1 else int(shoes_x)
        shoes_e = round(shoes_e) if shoes_e>1 else int(shoes_e)
        demage = list_demage[0]-(list_demage[0]/100*shoes_b) + list_demage[1]-(list_demage[1]/100*shoes_x) + list_demage[2]-(list_demage[2]/100*shoes_e)
        demage = round(demage) if demage>1 else int(demage)
        new_xp_shoes = xp_shoes-demage
        if new_xp_shoes > 0:
            new_percent_shoes = new_xp_shoes*100/dict_armor[shoes][4]
            new_percent_shoes = round(new_percent_shoes) if new_percent_shoes>1 else int(new_percent_shoes)
            logging.info(f'\nlist_demage = {list_demage}\nshoes_b = {shoes_b}\nshoes_x = {shoes_x}\nshoes_e = {shoes_e}\ndemage = {demage}\nnew_xp_shoes = {new_xp_shoes}\nnew_percent_shoes = {new_percent_shoes}')
            if new_percent_shoes > 0:
                await rq.set_user(tg_id=tg_id, name_column='shoes', current_value=f'{shoes}!{new_percent_shoes}')
                await rq.set_user(tg_id=tg_id, name_column='xp_shoes', current_value=new_xp_shoes)
                return [demage, shoes, new_percent_shoes]
            else:
                await rq.set_user(tg_id=tg_id, name_column='shoes', current_value='')
                return [demage, shoes, 0] # Если второй элемент существует, то эта броня уничтожена

    ### demage = суммируем и вычитаем из хп игрока
    demage = list_demage[0] + list_demage[1] + list_demage[2]
    new_xp_user = (data_user['xp']-demage) if (data_user['xp']-demage) > 0 else 0
    await rq.set_user(tg_id, 'xp', new_xp_user)
    return [demage]



#dict_gun: dict = {
#    'G17': [[0,0,0], [35,0,0], [45,0,10]], # дальний - средний - ближний /// баллистический - химический - электро
#    'spear': [[0,0,0], [0,0,0], [30,25,5]],
#    'nothink': [[0,0,0], [0,0,0], [5,2,0]],
#    }

#dict_NPS: dict = {
#    'luvron_polevoy': [[25, 10, 0], [5, 10, 5]], # первый список нападение, второй защита
#    'blue_rabbit': [[5, 3, 0], [2, 2, 5]],
#    'daron': [[5, 10, 35], [35, 15, 0], [25, 5, 25]], # первый и второй список нападение (среднее), третий защита
#}
async def demage_nps_subtracts_xp_gun(tg_id: int, name_nps: str, gun: str, distance: int, hand: str) -> int: # урон монстру в ХП
    """рассчет урона НПС, уменьшение ХП оружия, на выходе урон НПСа в ХП"""

    logging.info(f'demage_nps')

    dict_user = await rq.get_user_dict(tg_id=tg_id)
    # уменьшение хп оружия на одну единицу и удаление его из строки в БД, если ХП снизилось до нуля
    xp_gun = dict_user[f'xp_{hand}']
    logging.info(f'xp_gun = {xp_gun}')
    # gun и hand передаются на вход функции, gun лежит в hand
    if gun in ['G17', 'spear']: # уменьшение ХП оружия только у G17 и spear, у кулаков xp не уменьшается
        if xp_gun > 1:
            await rq.set_user(tg_id, f'xp_{hand}', xp_gun-1)
            logging.info(f'xp_gun = {xp_gun-1} ---------- xp_hand = xp_{hand}')
        else: # если хп 0, то оружие удаляется
            await rq.set_user(tg_id, hand, '')
            await rq.set_user(tg_id, f'xp_{hand}', 0)
            logging.info(f'xp_gun = {0}')

    demage_nps: int = 0
    for elem in range (3):
        logging.info(f'\ndemage_nps[{elem}] = {demage_nps}')
        demage_nps += ((100 - dict_NPS[name_nps][distance][elem])/100) * dict_gun[gun][-distance][elem]

    return demage_nps



async def change_xp_percent_and_back(name_thing: str, percent: int | None=None, xp: int | None=None) -> int:
    """переводит проценты в ХП или ХП в проценты"""
    logging.info(f'change_xp_percent_and_back')

    if percent:
        xp = round((dict_percent_xp[name_thing] / 100) *percent)
        logging.info(f'xp = {xp}')
        return xp
    if xp:
        percent = xp / (dict_percent_xp[name_thing] / 100)
        percent = round(percent) if percent >= 1 else int(percent)
        logging.info(f'percent = {percent}')
        return percent
