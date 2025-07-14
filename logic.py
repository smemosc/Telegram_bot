# logic.py
from database import get_all_user_data, save_data, get_user_data
from typing import Tuple


def determine_people_class(location: str, floor: int, total_floors: int, activity: str) -> str:
    """
    Новая логика:
      - Л4: в движущемся транспорте
      - Л3: вне помещений в движении/труде
      - Л2: вне помещений в покое
      - Л1: в помещении на 1/цокольном в покое
      - Л2: в помещении на 1/цокольном при активности
      - Л0: в помещении на верхних этажах 5–6
      - Л5/1: в помещении на других этажах в покое
      - Л5/2: в помещении на других этажах при активности
    """
    if location == 'В движущемся транспорте':
        return 'Л4'
    if location == 'Вне помещения':
        return 'Л3' if activity in ['ходьба', 'труд', 'движение'] else 'Л2'
    # location == 'В помещении'
    if total_floors in (5, 6) and floor >= 5:
        return 'Л0'
    if floor <= 1:
        return 'Л1' if activity == 'покой' else 'Л2'
    # остальные этажи
    return 'Л5/1' if activity == 'покой' else 'Л5/2'


def calculate_intensity(user_id: int) -> float:
    """
    Считает итоговую интенсивность как среднее арифметическое
    по непустым I_Л, IП и I_С, округлённое до 1 знака после запятой.
    """
    # читаем из БД
    i_l = get_user_data(user_id, 'I_Л')
    i_p = get_user_data(user_id, 'IП')
    i_c = get_user_data(user_id, 'I_С')

    # собираем только ненулевые/неNone
    vals = [v for v in (i_l, i_p, i_c) if v is not None]

    if not vals:
        return 0.0

    avg = sum(vals) / len(vals)
    # округляем до десятых
    return round(avg, 1)

# ------------------------------------------------------------------
# Таблица интерполяции для человека:
# ключ — 'Л0','Л1',…,'Л5/1','Л5/2', значение — список кортежей (I_Л, R_Л, W_Л).
# ------------------------------------------------------------------
INTERP_TABLE = {
    'Л0': [
        (0, 0.00, None),
        (1, 0.10, 1.00),
        (2, 0.30, 1.00),
        (3, 0.80, 0.00),
    ],
    'Л1': [
        (1, 0.00, 0.00),
        (2, 0.10, 0.70),
        (3, 0.30, 1.00),
        (4, 1.00, 1.00),
        (5, 2.20, 1.00),
        (6, 3.50, 1.00),
        (7, 4.50, 0.70),
        (8, 5.30, 0.00),
    ],
    'Л2': [
        (2, 0.00, 0.00),
        (3, 0.10, 0.70),
        (4, 0.50, 1.00),
        (5, 1.40, 1.00),
        (6, 2.90, 1.00),
        (7, 4.30, 0.70),
        (8, 5.00, 0.00),
        (9, 5.20, 0.70),
        (10,6.00, 0.00),
    ],
    'Л3': [
        (3, 0.00, 0.00),
        (4, 0.10, 0.70),
        (5, 0.50, 1.00),
        (6, 1.80, 1.00),
        (7, 3.40, 1.00),
        (8, 4.80, 0.70),
        (9, 5.20, 0.70),
        (10,1.00, 1.50),
        (11,0.70, 1.50),
    ],
    'Л4': [
        (1, 0.00, 0.00),
        (2, 0.10, 0.70),
        (3, 0.30, 1.00),
        (4, 1.00, 1.00),
        (5, 2.20, 1.00),
        (6, 3.50, 1.00),
        (7, 4.50, 0.70),
        (8, 5.30, 0.00),
        (9, 5.50, 0.00),
        (10,6.00, 0.00),
    ],
    'Л5/1': [
        (1, 0.00, 0.00),
        (2, 0.10, 0.70),
        (3, 0.30, 1.00),
        (4, 1.00, 1.00),
        (5, 2.20, 1.00),
        (6, 3.50, 1.00),
        (7, 4.50, 0.70),
        (8, 5.30, 0.00),
        (9, 5.20, 0.70),
        (10,1.00, 1.50),
        (11,0.70, 1.50),
    ],
    'Л5/2': [
        (1, 0.00, 0.00),
        (2, 0.10, 0.70),
        (3, 0.30, 1.00),
        (4, 1.00, 1.00),
        (5, 2.20, 1.00),
        (6, 3.50, 1.00),
        (7, 4.50, 0.70),
        (8, 5.30, 0.00),
        (9, 5.20, 0.70),
        (10,1.00, 1.50),
        (11,0.70, 1.50),
    ],
}


def interpolate_class(cls: str, r_value: float) -> Tuple[float, float]:
    """
    Линейная интерполяция по таблице INTERP_TABLE.
    Параметры:
      - cls — код класса ('Л0', 'Л1', …, 'Л5_1', 'Л5_2')
      - r_value — средняя реакция R_Л
    Возвращает (I_Л, W_Л), либо (0.0, 0.0) если данные отсутствуют.
    """
    key = cls.replace('/', '_')
    table = INTERP_TABLE.get(key)
    if not table:
        return 0.0, 0.0

    I0, R0, W0 = table[0]
    I1, R1, W1 = table[-1]

    if r_value <= R0:
        return I0, W0 or 0.0
    if r_value >= R1:
        return I1, W1 or 0.0

    for (I_prev, R_prev, W_prev), (I_curr, R_curr, W_curr) in zip(table, table[1:]):
        if R_prev <= r_value <= R_curr:
            t = (r_value - R_prev) / (R_curr - R_prev)
            I_lx = I_prev + t * (I_curr - I_prev)
            Wp = W_prev or 0.0
            Wc = W_curr or 0.0
            W_lx = Wp + (I_lx - I_prev) * (Wc - Wp)
            return I_lx, W_lx

    return 0.0, 0.0


# ------------------------------------------------------------------
# Таблица интерполяции для предметов (общая для всех П0–П5):
# список кортежей (I_П, R_П, W_П)
# ------------------------------------------------------------------
INTERP_ITEM_TABLE = [
    (0, 0.00, 0.00),
    (1, 0.15, 1.00),
    (2, 0.30, 1.00),
    (3, 0.90, 0.00),
    (4, 1.70, 0.70),
    (5, 2.60, 0.00),
    (6, 3.40, 0.70),
    (7, 5.00, 1.00),
    (8, 6.00, 1.00),
    (9, 7.00, 0.00),
    (10,8.00, 0.00),
    (11,9.00, 0.00),
]

INTERP_BUILDING = {
    5.0:  (0.0, 0.7),
    5.5:  (0.0, 1.0),
    6.0:  (4.0, 0.7),
    6.5:  (3.0, 0.7),
    7.0:  (2.0, 1.0),
    7.5:  (3.35,1.0),
    8.0:  (5.0, 0.7),
    9.0:  (5.0, 0.0),
    10.0: (5.0, 0.0),
    11.0: (4.0, 0.0),
}


def interpolate_item_class(item_cls: str, r_value: float) -> Tuple[float, float]:
    """
    Линейная интерполяция по общей таблице INTERP_ITEM_TABLE.
    item_cls здесь игнорируется (если вы захотите разные таблицы для П0–П5,
    то аналогично interpolate_class можно добавить словарь).
    """
    table = INTERP_ITEM_TABLE
    if not table:
        return 0.0, 0.0

    I0, R0, W0 = table[0]
    I1, R1, W1 = table[-1]

    if r_value <= R0:
        return I0, W0 or 0.0
    if r_value >= R1:
        return I1, W1 or 0.0

    for (I_prev, R_prev, W_prev), (I_curr, R_curr, W_curr) in zip(table, table[1:]):
        if R_prev <= r_value <= R_curr:
            t = (r_value - R_prev) / (R_curr - R_prev)
            I_px = I_prev + t * (I_curr - I_prev)
            Wp = W_prev or 0.0
            Wc = W_curr or 0.0
            W_px = Wp + (I_px - I_prev) * (Wc - Wp)
            return I_px, W_px

    return 0.0, 0.0

def interpolate_building(c_total: float) -> Tuple[float, float]:
    """
    Линейная интерполяция по INTERP_BUILDING.
    Если c_total вне диапазона, берём крайнее.
    """
    # Отсортируем узлы
    nodes = sorted(INTERP_BUILDING.items())  # [(5.0,(I,W)), (5.5,..), ...]
    # ниже минимального
    if c_total <= nodes[0][0]:
        return nodes[0][1]
    # выше максимального
    if c_total >= nodes[-1][0]:
        return nodes[-1][1]
    # ищем между
    for (c0,(I0,W0)), (c1,(I1,W1)) in zip(nodes, nodes[1:]):
        if c0 <= c_total <= c1:
            t = (c_total - c0) / (c1 - c0)
            I = I0 + t*(I1 - I0)
            W = W0 + (I - I0)*( (W1 or 0) - (W0 or 0) )
            return I, W
    # на всякий случай
    return 0.0, 0.0


def calculate_item_stats(user_id: int):
    data = get_all_user_data(user_id)
    sum_r, sum_i, sum_w = 0.0, 0.0, 0.0

    for i in range(6):  # Для П0–П5
        r = data.get(f'RП{i}')
        if r is not None:
            I_i, W_i = interpolate_item_class(f'П{i}', r)
            save_data(user_id, **{
                f'IП{i}': I_i,
                f'WП{i}': W_i
            })
            sum_r += r * W_i
            sum_i += I_i * W_i
            sum_w += W_i

    # Если суммарный вес нулевой — присваиваем ноль, иначе считаем взвешенное
    if sum_w == 0:
        save_data(user_id, RП=0.0, IП=0.0)
    else:
        save_data(
            user_id,
            RП=sum_r / sum_w,
            IП=sum_i / sum_w
        )
