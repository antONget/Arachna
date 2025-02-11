from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import async_session, User, StorageGun, StorageBIO, StorageTrash, StorageWardrobe


from lexicon.lexicon_ru import (LEXICON_Invite, LEXICON_BUTTON as LBut, LEXICON_STORAGE_TRASH as LST,
                                LEXICON_ALL_THINGS as All_Th, list_storage_wardrobe_gun as LSWG)

import database.help_function as hf
import database.requests as rq
from database.help_function import Backpack, Location

import logging


"""
def kb_begin() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="Начать")
    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True)
    return keyboard
"""

### Зачем два префикса? Как это применять?
def create_in_kb(width: int,
                 **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for button, callback_data in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=callback_data))
    kb_builder.row(*buttons, width=width)
     # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_in_kb_from_list_dict(
        list_dict: list
) -> InlineKeyboardMarkup:
    logging.info(f'create_in_kb_from_list_dict') # [[{}],[{},{}],[],[]]
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for list_ in list_dict:  #[{}] заходим в первый элемент листа, спрашиваем сколько словарей в нем
        len_list = len(list_)
        #logging.info(f'list_ = {list_} --- len_list = {len_list}')
        for dict_ in list_:
            for key, item in dict_.items():
                buttons.append(
                    InlineKeyboardButton(
                        text=key,
                        callback_data=item
                    )
                )
        kb_builder.row(*buttons, width=len_list)
        buttons: list[InlineKeyboardButton] = []
    return kb_builder.as_markup()




def create_list_in_kb(width: int, dict_: dict, prefix1: str| None=None,
                      prefix2: str | None=None, clb_back_str: str | None=None,
                      backpack_clb_back: str | None=None,
                      take_all_: str | None=None, do_not_take_: str | None=None,) -> InlineKeyboardMarkup: #  do_not_take_{loot}  do_not_take_{hunt}
    logging.info(f'create_list_in_kb')
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key, item in dict_.items():

        if int(dict_[key])>0:

            text = All_Th[key]
            button = f"{prefix1}!{key}"
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
            #if key in LSWG:
            #    per = '%'
            #else:
            #    per = 'шт.'
            text = f"{item} шт."#{per}"
            button = f"{prefix2}!{key}!{item}"
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))


    kb_builder.row(*buttons, width=width)

    if backpack_clb_back:
        button_backpack = InlineKeyboardButton(text='Рюкзак',
                                           callback_data=backpack_clb_back)
        kb_builder.row(button_backpack)



    if take_all_:
        button_take_all_loot = InlineKeyboardButton(text='взять всё',
                                           callback_data=f'take_all_{take_all_}') # отличается loot и hunt
        kb_builder.row(button_take_all_loot)

    if do_not_take_:
        button_do_not_take_loot = InlineKeyboardButton(text='не брать',
                                           callback_data=f'do_not_take_{do_not_take_}') # отличается loot и hunt
        kb_builder.row(button_do_not_take_loot)

    if clb_back_str:
        button_back = InlineKeyboardButton(text=LBut['back'],
                                           callback_data=clb_back_str)
        kb_builder.row(button_back)

    return kb_builder.as_markup()



def create_list_in_one_row_kb_repair(
        dict_: dict,
        prefix: str| None=None,
        clb_back_str: str | None=None) -> InlineKeyboardMarkup:
    logging.info(f'create_list_in_one_row_kb_repair')
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key, item in dict_.items():

        if int(dict_[key])>0:

            text = f'{All_Th[key]} {item} шт'
            button = f"{prefix}!{key}"
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    kb_builder.row(*buttons, width=1)

    if clb_back_str:
        button_back = InlineKeyboardButton(text='Назад',
                                           callback_data=clb_back_str)
        kb_builder.row(button_back)

    return kb_builder.as_markup()



def create_keyboard_from_colored_cell(list_pocket: list = [],
                                      list_cell: list = [],
                                      clb_back: str = '')-> InlineKeyboardMarkup:
    """
    клавиатура из цветных ячеек
    """
    logging.info(f'create_keyboard_from_colored_cell')
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if list_pocket:
        logging.info(f'list_pocket = {list_pocket}')
        for list_inside in list_pocket:
            logging.info(f'list_inside = {list_inside}')
            text = list_inside[0]
            button = list_inside[1]
            #logging.info(f"len(button.encode('utf-8') = {len(button.encode('utf-8'))}")
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
        kb_builder.row(*buttons)
    if list_cell:
        buttons.clear()
        for list_inside in list_cell:
            text = list_inside[0]
            button = list_inside[1]
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
        kb_builder.row(*buttons)
        #logging.info(f'ВРЕМЕННО 124 buttons = {buttons}')
    if clb_back:
        button_back = InlineKeyboardButton(text='Назад',
                                           callback_data=clb_back)

        kb_builder.row(button_back)
    return kb_builder.as_markup()



def create_kb_from_1_to_9_with_all(prefix1:str, clb_back: str, clb_name: str = '') -> InlineKeyboardMarkup:
    logging.info(f'create_kb_from_1_to_9_with_all')
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in range(1,10):
        buttons.append(InlineKeyboardButton(
            text=f"[{str(i)}]",
            callback_data=f"{prefix1}!{clb_name}!{str(i)}"
        ))
    button_all = InlineKeyboardButton(text=LBut['all'], callback_data=f"{prefix1}!{clb_name}!all")
    button_back = InlineKeyboardButton(text=LBut['back'], callback_data=clb_back)
    kb_builder.row(*buttons, width=3)
    kb_builder.row(button_all)
    kb_builder.row(button_back)
    return kb_builder.as_markup()

def create_kb_from_1_to_0_with_ok(prefix1:str, clb_back: str, clb_name: str = '') -> InlineKeyboardMarkup:
    logging.info(f'create_kb_from_1_to_0_with_ok')
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in range(1,10):
        buttons.append(InlineKeyboardButton(
            text=f"[{str(i)}]",
            callback_data=f"{prefix1}!{clb_name}!{str(i)}"
        ))
    button_null = InlineKeyboardButton(text='0', callback_data=f"{prefix1}!{clb_name}!{0}")
    button_ok = InlineKeyboardButton(text=LBut['ok'], callback_data=f"ok!{clb_name}")
    button_back = InlineKeyboardButton(text=LBut['back'], callback_data=clb_back)
    kb_builder.row(*buttons, width=3)
    kb_builder.row(button_null, button_ok)
    kb_builder.row(button_back)
    return kb_builder.as_markup()

#[['[Усиленный шлем 1 шт. 7%]', 'ward2!helmet_reinforced!1!7'], ['[Усиленный шлем 1 шт. 6%]', 'ward2!helmet_reinforced!1!6'],
# ['[Усиленный шлем 1 шт. 5%]', 'ward2!helmet_reinforced!1!5'], ['[Усиленный шлем 1 шт. 4%]', 'ward2!helmet_reinforced!1!4'],
# ['[Усиленный шлем 1 шт. 3%]', 'ward2!helmet_reinforced!1!3'], ['[Усиленный шлем 1 шт. 2%]', 'ward2!helmet_reinforced!1!2'],
# ['[Усиленный шлем 1 шт. 1%]', 'ward2!helmet_reinforced!1!1']]



# клавиатура для пагинации
def create_kb_from_list_to_placement_more_then_lenth_step_button(
        list_button: list,
        back: int,
        forward: int,
        count:int,
        clb_name: str,
        clb_button_back: str,
        prefix_wardrobe: str)->InlineKeyboardMarkup:
    logging.info('create_kb_from_list_to_placement_more_then_lenth_step_button')

    # проверка чтобы не ушли в минус
    if back < 0:
        back = 0
        forward = 2

    # считаем сколько всего блоков по заданному количеству элементов в блоке
    count_buttons = len(list_button)
    whole = count_buttons // count
    remains = count_buttons % count
    max_forward = whole + 1
    # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    if forward > max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for inside_list in list_button[back*count:(forward-1)*count]:
        text = inside_list[0]
        button = inside_list[1]
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    kb_builder.row(*buttons, width=1)
    if len(list_button) < 5:
        button_go_away = InlineKeyboardButton(text='Назад',
                                            callback_data=clb_button_back)
    else:
        button_back = InlineKeyboardButton(text='Обратно',
                                        callback_data=f'{prefix_wardrobe}_back!{str(back)}!{clb_name}')
        button_go_away = InlineKeyboardButton(text='Назад',
                                            callback_data=clb_button_back)
        button_next = InlineKeyboardButton(text='Далее',
                                        callback_data=f'{prefix_wardrobe}_forward!{str(forward)}!{clb_name}')
        kb_builder.row(button_back, button_next)

    kb_builder.row(button_go_away)
### РАБОТАЕТ!!! ТУТ НАДО ПОСТАВИТЬ ЛОГГИНГ И СПРАШИВАТЬ КАКАЯ ПЕРЕМЕННАЯ ЧЕМУ РАВНА И
### И НАЙТИ ТЕ УСЛОВИЯ ЧТОБЫ ДОБАВЛЯТЬ ПРАВИЛЬНО КНОПКИ ДАЛЕЕ----ОБРАТНО
    return kb_builder.as_markup()



async def create_kb_show_cells_backpack(tg_id: int, prefix: str, clb_back: str) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру в зависимости от надетого рюкзака и его содержимого
    """
    logging.info(f"create_kb_show_cells_backpack")

    pocket1 = await rq.get_Pocket1(tg_id=tg_id)
    pocket2 = await rq.get_Pocket2(tg_id=tg_id)



    data_backpack = await hf.what_backpack_put_on(tg_id=tg_id) # какой рюкзак надет?
    if '!' in data_backpack:
        backpack = data_backpack.split('!')[0] # в User[backpack] запись: 'no_backpack' или 'backpack_foliage!100'
    else:
        backpack = data_backpack

    if pocket1:
        button_pocket1 = InlineKeyboardButton(
            text=f"[{LST[list(pocket1.items())[0][0]]} {list(pocket1.items())[0][1]}шт]",
            callback_data=f"{prefix}!{backpack}!pocket1!{list(pocket1.items())[0][0]}!{list(pocket1.items())[0][1]}")
    else:
        button_pocket1 = InlineKeyboardButton(
            text=f"[Пусто]",
            callback_data=f"{prefix}!{backpack}!pocket1!Пусто!0")

    if pocket2:
        button_pocket2 = InlineKeyboardButton(
            text=f"[{LST[list(pocket2.items())[0][0]]} {list(pocket2.items())[0][1]}шт]",
            callback_data=f"{prefix}!{backpack}!pocket2!{list(pocket2.items())[0][0]}!{list(pocket2.items())[0][1]}")
    else:
        button_pocket2 = InlineKeyboardButton(
            text=f"[Пусто]",
            callback_data=f"{prefix}!{backpack}!pocket2!Пусто!0")
    button_back = InlineKeyboardButton(text='Назад', callback_data=clb_back)

# Если рюкзака нет, то нет смысла идти дальше, показываем только карманы
    if backpack == Backpack.no_backpack:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_pocket1, button_pocket2], [button_back]]
        )
        return keyboard


# Если надет ЛИСТВЕННЫЙ рюкзак
    elif backpack == Backpack.backpack_foliage:
        cell_1 = await rq.get_BFoliageCell_1(tg_id=tg_id)
        cell_2 = await rq.get_BFoliageCell_2(tg_id=tg_id)
        bio = (await rq.get_BackpackFoliage(tg_id=tg_id))['bio'] # Кнопка био
        if cell_1:
            if list(cell_1.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_1 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_1.items())[0][0]]} {list(cell_1.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_1!{list(cell_1.items())[0][0]}!{list(cell_1.items())[0][1]}")
        else:
            button_cell_1 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_1!Пусто!0")

        if cell_2:
            if list(cell_2.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_2 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_2.items())[0][0]]} {list(cell_2.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_2!{list(cell_2.items())[0][0]}!{list(cell_2.items())[0][1]}")
        else:
            button_cell_2 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_2!Пусто!0")


    # Если надет ЛЕАННЫЙ рюкзак
    elif backpack == Backpack.backpack_leana:
        cell_1 = await rq.get_BLeanaCell_1(tg_id=tg_id)
        cell_2 = await rq.get_BLeanaCell_2(tg_id=tg_id)
        cell_3 = await rq.get_BLeanaCell_3(tg_id=tg_id)
        cell_4 = await rq.get_BLeanaCell_4(tg_id=tg_id)
        bio = (await rq.get_BackpackLeana(tg_id=tg_id))['bio'] # Кнопка био

        if cell_1:
            if list(cell_1.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_1 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_1.items())[0][0]]} {list(cell_1.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_1!{list(cell_1.items())[0][0]}!{list(cell_1.items())[0][1]}")
        else:
            button_cell_1 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_1!Пусто!0")

        if cell_2:
            if list(cell_2.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_2 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_2.items())[0][0]]} {list(cell_2.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_2!{list(cell_2.items())[0][0]}!{list(cell_2.items())[0][1]}")
        else:
            button_cell_2 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_2!Пусто!0")

        if cell_3:
            if list(cell_3.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_3 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_3.items())[0][0]]} {list(cell_3.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_3!{list(cell_3.items())[0][0]}!{list(cell_3.items())[0][1]}")
        else:
            button_cell_3 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_3!Пусто!0")

        if cell_4:
            if list(cell_4.keys())[0] in LSWG:
                per = '%'
            else:
                per = 'шт'
            button_cell_4 = InlineKeyboardButton(
                text=f"[{All_Th[list(cell_4.items())[0][0]]} {list(cell_4.items())[0][1]}{per}]",
                callback_data=f"{prefix}!{backpack}!cell_4!{list(cell_4.items())[0][0]}!{list(cell_4.items())[0][1]}")
        else:
            button_cell_4 = InlineKeyboardButton(
                text=f"[Пусто]",
                callback_data=f"{prefix}!{backpack}!cell_4!Пусто!0")

    button_bio = InlineKeyboardButton(
            text=f"[био {bio}]",
            callback_data=f"{prefix}!{backpack}!био!clb_for_bio!{bio}"
        )

    if backpack == Backpack.backpack_foliage:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_bio], [button_pocket1, button_pocket2], [button_cell_1, button_cell_2], [button_back]]
        )
    elif backpack == Backpack.backpack_leana:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_bio], [button_pocket1, button_pocket2], [button_cell_1, button_cell_2], [button_cell_3, button_cell_4], [button_back]]
        )

    return keyboard



# Возвращает клавиатуру в зависимости от действия, количества вещей в ячейке и в хранилищах
async def create_kb_to_remove_backpack_to_storage_and_back(
        tg_id: int | None=None,
        value_pocket_cell: int | None=None, # для ПЕРЕЛОЖИТЬ имеет значение value_from_pc
        value_storage: int | None=None,
        value_to_pc: int | None=None,
        prefix: str = ' ',
        clb_action: str = ' ' ,
        clb_backpack: str = ' ' ,
        clb_pocket_cell: str = ' ' , # для ПЕРЕЛОЖИТЬ == clb_from_pc
        clb_to_pc: str | None=None,
        clb_name: str = ' ' ,
        clb_back: str = ' ',
        ) -> list:
    """
    Возвращает клавиатуру в зависимости от действия, количества вещей в ячейке и в хранилищах,
    """
    logging.info(f"create_kb_to_remove_backpack_storage_and_back")


    #kb_dict_back = {LBut['back']: f"tr2!put_in_backpack!{clb_name}"}
    kb_dict_only_1=             {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            'Назад': clb_back}
    kb_dict_1_all =             {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                '[Все]': f"{prefix}!333!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            'Назад': clb_back}
    kb_dict_1_2_all =           {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                '[Все]': f"{prefix}!333!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            'Назад': clb_back}
    kb_dict_1_2_5_all =         {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[Все]': f"{prefix}!333!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                             'Назад': clb_back}
    kb_dict_1_2_5_10_all =      {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[10]': f"{prefix}!10!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[Все]': f"{prefix}!333!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                             'Назад': clb_back}


    kb_dict_to_the_full_10 =    {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[10]': f"{prefix}!10!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                  'До полного': f"{prefix}!777!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            'Назад': clb_back}
    kb_dict_to_the_full_5 =     {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'До полного': f"{prefix}!777!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                             'Назад': clb_back}
    kb_dict_to_the_full_2 =     {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'До полного': f"{prefix}!777!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'Назад': clb_back}
    kb_dict_to_the_full_1 =     {'[1]': f"tr4!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                'До полного': f"tr4!777!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            'Назад': clb_back}

    # Клавиатуры для действия ПЕРЕЛОЖИТЬ (Если в двух ячейках в сумме > 20, то кнопка "Все" не нужна)
    kb_dict_1_2 =               {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'Назад': clb_back}
    kb_dict_1_2_5 =             {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'Назад': clb_back}
    kb_dict_1_2_5_10 =          {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[2]': f"{prefix}!2!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[5]': f"{prefix}!5!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 '[10]': f"{prefix}!10!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                 'Назад': clb_back}



# ПОЛОЖИТЬ В ХРАНИЛИЩЕ
    if clb_action == 'put_in_storage': # положить в хранилище
        logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action == 'put_in_storage':")
        if clb_name not in LSWG: # Для брони / оржия своя клавиатура, т.к. предметы по одному лежат
            if value_pocket_cell == 20: # для разных количеств вещей в ячейке своя клавиатура
                kb_dict = kb_dict_1_2_5_10_all
                keyboard = create_in_kb(4, **kb_dict)
            elif 5 < value_pocket_cell <= 20:
                kb_dict = kb_dict_1_2_5_all
                keyboard = create_in_kb(3, **kb_dict)
            elif 2 < value_pocket_cell <= 5:
                kb_dict = kb_dict_1_2_all
                keyboard = create_in_kb(2, **kb_dict)
            elif value_pocket_cell == 2:
                kb_dict = kb_dict_1_all
                keyboard = create_in_kb(2, **kb_dict)
            elif value_pocket_cell == 1:
                kb_dict = kb_dict_only_1
                keyboard = create_in_kb(2, **kb_dict)
            else: #### Это сделано, чтобы в любом случае всплывала клавиатура
                kb_dict = kb_dict_only_1
                keyboard = create_in_kb(2, **kb_dict)

        else: # Для брони / оржия своя клавиатура
            kb_dict = kb_dict_only_1
            keyboard = create_in_kb(2, **kb_dict)
            logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action == 'put_in_storage': keyboard = {keyboard}")
        return keyboard

# ВЫКИНУТЬ
    elif clb_action == 'throw_it_out': # выкинуть
        logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action == 'throw_it_out':")
        if clb_name not in LSWG: # Для брони / оржия своя клавиатура, т.к. предметы по одному лежат
            if value_pocket_cell == 20: # для разных количеств вещей в ячейке своя клавиатура
                kb_dict = kb_dict_1_2_5_10_all
                keyboard = create_in_kb(4, **kb_dict)
            elif 5 < value_pocket_cell <= 20:
                kb_dict = kb_dict_1_2_5_all
                keyboard = create_in_kb(3, **kb_dict)
            elif 2 < value_pocket_cell <= 5:
                kb_dict = kb_dict_1_2_all
                keyboard = create_in_kb(2, **kb_dict)
            elif value_pocket_cell == 2:
                kb_dict = kb_dict_1_all
                keyboard = create_in_kb(2, **kb_dict)
            elif value_pocket_cell == 1:
                kb_dict = kb_dict_only_1
                keyboard = create_in_kb(2, **kb_dict)
        else: # Для брони / оржия своя клавиатура
            kb_dict = kb_dict_only_1
            keyboard = create_in_kb(2, **kb_dict)
        return keyboard

# ДОЛОЖИТЬ В РЮКЗАК
### Скорее всего надо сделать проверку, что доложить в рюкзак можно только трэш
    elif clb_action == 'dologit': # положить в рюкзак
        logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action == 'dologit'--- clb_action == {clb_action}")
        logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action --- \n value_storage = {value_storage} {type(value_storage)}\nvalue_pocket_cell = {value_pocket_cell} {type(value_pocket_cell)}")

        if value_storage+value_pocket_cell >= 20: # "до полного" в хранилище должно быть больше либо равно, чем можно положить
            if 0 <= value_pocket_cell< 15: #      # для разных количеств свободного места в ячейке своя клавиатура "до полного"
                kb_dict = kb_dict_to_the_full_5
                keyboard = create_in_kb(3, **kb_dict)
                logging.info(f'if value_storage + value_pocket_cell >= 20:')
            elif 15 <= value_pocket_cell< 18: #
                kb_dict = kb_dict_to_the_full_2
                keyboard = create_in_kb(2, **kb_dict)
                logging.info(f'elif 15 <= value_pocket_cell< 18:')
            elif value_pocket_cell== 18: #
                kb_dict = kb_dict_to_the_full_1
                keyboard = create_in_kb(2, **kb_dict)
                logging.info(f'elif value_pocket_cell== 18:')
            elif value_pocket_cell== 19: #
                kb_dict = kb_dict_only_1
                keyboard = create_in_kb(1, **kb_dict)
                logging.info(f'elif value_pocket_cell== 19:')
            return keyboard


        elif value_storage+value_pocket_cell< 20: # Здесь "до полного" быть не может. Только "Все".
            logging.info(f'ВНИМАНИЕ!!! ПОМЕНЯЛ if 1 <= value_pocket_cell< 15: на if 0 <= value_pocket_cell< 15:value_storage = {value_storage} --- value_pocket_cell = {value_pocket_cell}')
            if 0 <= value_pocket_cell< 15: ### if 1 <= value_pocket_cell< 15:
                if value_storage >= 5: #
                    kb_dict = kb_dict_1_2_5_all
                    keyboard = create_in_kb(3, **kb_dict)
                    logging.info(f'elif value_storage+value_pocket_cell< 20: if 1 <= value_pocket_cell< 15: if value_storage == 5: ')
                elif 2 <= value_storage < 5: #
                    kb_dict = kb_dict_1_2_all
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif value_storage+value_pocket_cell< 20: if 1 <= value_pocket_cell< 15: elif 2<= value_storage < 5:')
                elif value_storage == 1: #
                    kb_dict = kb_dict_1_all
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif value_storage+value_pocket_cell< 20: if 1 <= value_pocket_cell< 15: elif value_storage == 1:')

            elif 15 <= value_pocket_cell< 18:
                if 2 <= value_storage < 5: #
                    kb_dict = kb_dict_1_2_all
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif value_storage+value_pocket_cell< 20:  elif 15 <= value_pocket_cell< 18: if 2 <= value_storage < 5')
                elif value_storage == 1: # +
                    kb_dict = kb_dict_1_all
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif value_storage+value_pocket_cell< 20:  elif 15 <= value_pocket_cell< 18: elif value_storage == 1')

            elif value_pocket_cell== 18: #
                kb_dict = kb_dict_1_all
                keyboard = create_in_kb(2, **kb_dict)
                logging.info(f'elif value_storage+value_pocket_cell< 20: elif value_pocket_cell== 18')
            return keyboard

# ПЕРЕЛОЖИТЬ
    elif clb_action == 'perelogit':
        logging.info(f"create_kb_to_remove_backpack_storage_and_back elif clb_action == 'perelogit'--- clb_action == {clb_action} --- clb_name = {clb_name}")

        if clb_name not in LSWG: # Клавиатуры снизу только для ХЛАМА
            if value_pocket_cell+value_to_pc > 20: # Нельзя чтобы были кнопки "Все", а то будет перебор
                logging.info(f'if value_to_pc + value_pocket_cell > 20:')
                if 1 <= value_to_pc< 10: #      # для разных количеств свободного места в ячейке своя клавиатура "до полного"
                    kb_dict = kb_dict_1_2_5_10
                    keyboard = create_in_kb(4, **kb_dict)
                    logging.info(f'if 1 <= value_to_pc< 10')
                elif 10 <= value_to_pc< 15: #
                    kb_dict = kb_dict_1_2_5
                    keyboard = create_in_kb(3, **kb_dict)
                    logging.info(f'elif 10 <= value_to_pc< 15:')
                elif 15 <= value_to_pc<=18: #
                    kb_dict = kb_dict_1_2
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif 15 <= value_to_pc<=18:')
                elif value_to_pc== 19: #
                    kb_dict = kb_dict_only_1
                    keyboard = create_in_kb(1, **kb_dict)
                    logging.info(f'elif value_to_pc== 19:')
                return keyboard

            elif value_pocket_cell+value_to_pc <= 20: # Есть кнопки "Все"
                logging.info(f'if value_to_pc ({value_to_pc}) + value_pocket_cell ({value_pocket_cell}) < 20:')
                if value_pocket_cell== 1:
                    kb_dict = kb_dict_only_1
                    keyboard = create_in_kb(1, **kb_dict)
                    logging.info(f'elif value_to_pc+value_pocket_cell< 20: if value_pocket_cell== 1: ')

                elif 2 <= value_pocket_cell < 5:
                    kb_dict = kb_dict_1_2_all
                    keyboard = create_in_kb(2, **kb_dict)
                    logging.info(f'elif value_to_pc+value_pocket_cell< 20: elif 2 <= value_pocket_cell < 5: ')

                elif 5 <= value_pocket_cell < 10:
                    #if value_to_pc >= 5: # value_pocket_cell
                    kb_dict = kb_dict_1_2_5_all
                    keyboard = create_in_kb(4, **kb_dict)
                    logging.info(f'elif value_to_pc+value_pocket_cell< 20:   elif 5 <= value_pocket_cell < 10: ')


                elif 10 <= value_pocket_cell<= 20:
                    logging.info(f'НУ И ЧТО? elif value_to_pc+value_pocket_cell< 20:  elif 15 <= value_pocket_cell<= 20:')

                    if 0 <= value_to_pc <= 10: #
                        kb_dict = kb_dict_1_2_5_10_all
                        keyboard = create_in_kb(4, **kb_dict)
                        logging.info(f'kb_dict = {kb_dict} --- elif value_to_pc+value_pocket_cell< 20:  elif 15 <= value_pocket_cell<= 20: if 0 <= value_to_pc <= 10:')
                    elif 10 < value_to_pc <= 15: #
                        kb_dict = kb_dict_1_2_5_all
                        keyboard = create_in_kb(3, **kb_dict)
                        logging.info(f'elif value_to_pc+value_pocket_cell< 20:  elif 15 <= value_pocket_cell<= 20: elif 10 < value_to_pc <= 15:')
                    elif 15 < value_to_pc <= 18: #
                        kb_dict = kb_dict_1_2_all
                        keyboard = create_in_kb(2, **kb_dict)
                        logging.info(f'elif value_to_pc+value_pocket_cell< 20:  elif 15 <= value_pocket_cell<= 20: elif 15 < value_to_pc <= 18:')
                    else:
                        kb_dict = kb_dict_only_1
                        keyboard = create_in_kb(1, **kb_dict)
                        logging.info(f'elif value_to_pc+value_pocket_cell< 20:  elif 15 <= value_pocket_cell<= 20: else:')
                #elif 18<=value_pocket_cell<= 20: #
                #    kb_dict = kb_dict_1_all
                #    keyboard = create_in_kb(2, **kb_dict)
                #    logging.info(f'elif value_to_pc+value_pocket_cell< 20: elif value_pocket_cell== 18')

        else: # Для брони / оржия своя клавиатура
            # kb_dict_only_1=             {'[1]': f"{prefix}!1!{clb_action}!{clb_backpack}!{clb_pocket_cell}!{clb_name}!{value_pocket_cell}",
                                            #'Назад': clb_back}
            kb_dict = kb_dict_only_1
            logging.info(f'kb_dict = {kb_dict}')
            keyboard = create_in_kb(2, **kb_dict)
        return keyboard
