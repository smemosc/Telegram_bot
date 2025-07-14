from enum import IntEnum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Токен вашего бота
TOKEN = "7740129001:AAEjxwl4cf8EJxV7UR-IjdiPCUwjPy8Iua4"

class States(IntEnum):
    DATE                    = 1
    TIME                    = 2
    ADDRESS                 = 3
    LOCATION                = 4
    FLOOR_NUMBER            = 5
    BUILDING_FLOORS         = 6
    ACTIVITY                = 7
    PEOPLE_REACTION         = 8
    CUSTOM_PEOPLE_REACTION  = 9
    SELECT_ITEM_REACTION    = 10
    BUILDING_CLASS          = 11
    DAMAGE_CRACKS           = 12
    DAMAGE_PLASTER          = 13
    DAMAGE_STRUCTURAL       = 14
    DAMAGE_OVERALL          = 15
    BUILDING_TECH_STATE     = 16
    BUILDING_YEAR           = 17
    BUILDING_SHAPE          = 18
    BUILDING_DIFF           = 19
    CUSTOM_BUILDING_DAMAGE  = 20

# Описания классов людей (для get_people_class_description, не трогаем)
PEOPLE_CLASSES = {
    'Л0': "На верхних этажах 5-,6-этажных зданий",
    'Л1': "В помещении на 1/цокольном в покое",
    'Л2': "В помещении на 1/цокольном при активности; либо вне помещений в покое",
    'Л3': "Вне помещений в движении/физическом труде",
    'Л4': "В движущемся транспорте",
    'Л5/1': "В помещении на других этажах в покое",
    'Л5/2': "В помещении на других этажах при активности"
}

REACTIONS_BY_CLASS = {
    'Л0': [
        ("не почувствовали, не заметили, не реагировали",         0),
        ("ощутили слегка, испытали легкое недоумение, не меняя поведение", 1),
        ("ощутили заметно; обратили внимание; оценили направление и длительность", 2),
        ("ощутили лёгкий испуг",                                 3),
        ("ощутили сильный испуг; хотелось выбежать из помещения",4),
        ("запаниковали; кричали, потеряли равновесие",           5),
        ("полностью утратили осмысленность, дезориентированы, отключение",6),
    ],
    'Л1': [
        ("не почувствовали, не заметили, не реагировали",         0),
        ("ощутили слегка, испытали легкое недоумение, не меняя поведение", 1),
        ("ощутили заметно; обратили внимание; оценили направление и длительность", 2),
        ("ощутили лёгкий испуг",                                 3),
        ("ощутили сильный испуг; хотелось выбежать из помещения",4),
        ("запаниковали; кричали, потеряли равновесие",           5),
        ("полностью утратили осмысленность, дезориентированы, отключение",6),
    ],
    'Л2': [
        ("не почувствовали, не заметили, не реагировали",                                               0),
        ("ощутили слегка; проснулись спокойно, не осознавая причины",                                    1),
        ("ощутили заметно; проснулись с ощущением, что кто-то разбудил",                                 2),
        ("ощутили лёгкий испуг",                                                                         3),
        ("ощутили сильный испуг; хотелось выбежать из помещения",                                       4),
        ("запаниковали; кричали, потеряли равновесие",                                                   5),
        ("полностью утратили осмысленность, дезориентированы, отключение",                              6),
    ],
    'Л3': [
        ("не почувствовали, не заметили, не реагировали",         0),
        ("ощутили слегка, не меняя поведение",                   1),
        ("ощутили заметно; обратили внимание; оценили направление и длительность", 2),
        ("ощутили лёгкий испуг",                                 3),
        ("ощутили сильный испуг",                                4),
        ("запаниковали; потеряли равновесие",                    5),
        ("полностью утратили осмысленность, дезориентированы, отключение",6),
    ],
    'Л4': [
        ("не почувствовали, не заметили, не реагировали",                                               0),
        ("ощутили слегка; относили за счет неровностей дороги",                                          1),
        ("ощутили заметно; ощутили несоответствие поведения авто особенностям дороги",                   2),
        ("ощутили лёгкий испуг; появились мысли об аварии",                                             3),
        ("ощутили сильный испуг; остановили авто",                                                      4),
        ("запаниковали; кричали",                                                                       5),
        ("полностью утратили осмысленность, дезориентированы, отключение",                              6),
    ],
    'Л5/1': [
        ("не почувствовали, не заметили, не реагировали",         0),
        ("ощутили слегка, не меняя поведение",                   1),
        ("ощутили заметно; оценили направление и длительность",  2),
        ("ощутили лёгкий испуг",                                 3),
        ("ощутили сильный испуг; хотелось выбежать",             4),
        ("запаниковали; потеряли равновесие",                    5),
        ("полностью утратили осмысленность, дезориентированы",   6),
        ("ударялись о стены и предметы, выпали из окна",         7),
    ],
    'Л5/2': [
        ("не почувствовали, не заметили, не реагировали",                                               0),
        ("ощутили слегка; проснулись спокойно, не осознавая причины",                                    1),
        ("ощутили заметно; проснулись с ощущением, что кто-то разбудил",                                 2),
        ("ощутили лёгкий испуг",                                                                         3),
        ("ощутили сильный испуг; хотелось выбежать",                                                     4),
        ("запаниковали; потеряли равновесие",                                                            5),
        ("полностью утратили осмысленность, дезориентированы, отключение",                              6),
        ("ударялись о стены и предметы, не попадали в двери, выпали из окна",                            7),
    ],
}


# Реакции людей
PEOPLE_REACTIONS = {
    0: "Отсутствие реакции",
    1: "Слабое ощущение",
    2: "Сильное ощущение",
    3: "Испуг",
    4: "Сильный испуг",
    5: "Паника",
    6: "Отключение"
}

# Классы предметов
ITEM_CLASSES = {
    'П0': "Предметы на верхних этажах 5-,6-этажных зданий",
    'П1': "Свободно висящие предметы (лампы, люстры)",
    'П2': "Неустойчивые подвижные предметы (игрушки, посуда)",
    'П3': "Устойчивые подвижные предметы (книги, легкая мебель)",
    'П4': "Тяжелые подвижные предметы (холодильники, техника)",
    'П5': "Малоподвижные предметы (сейфы, пианино)"
}

# Реакции предметов
ITEM_REACTIONS = {
    -1: "Не определено",
     0: "Отсутствие реакции",
     1: "Слабая реакция",
     2: "Сильная реакция"
}

# Классы сейсмостойкости зданий
BUILDING_CLASSES = {
    'С6': "Глинобитное, саманное, из камней или крупных блоков, связанных глиняным раствором, без каркаса и фундамента",
    'С7': "Деревянное или щитовое; саманное, кирпичное, блочное на цементном растворе; панельное, бетонное",
    'С8': "Любого вида с антисейсмическим усилением на 8 баллов",
    'С9': "Любого вида с антисейсмическим усилением на 9 баллов"
}

# Техническое состояние здания до землетрясения
BUILDING_CONDITIONS = {
    "Неизвестно, Нормативное, Работоспособное": 0,
    "Ограниченно-работоспособное":             -1,
    "Аварийное":                               -2
}

class Keyboards:
    @staticmethod
    def location():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("В помещении", callback_data="loc_in")],
            [InlineKeyboardButton("Вне помещения", callback_data="loc_out")],
            [InlineKeyboardButton("В транспорте", callback_data="loc_trans")]
        ])

    @staticmethod
    def activity():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("покой", callback_data="act_покой"),
                InlineKeyboardButton("движение", callback_data="act_движение"),
                InlineKeyboardButton("труд", callback_data="act_труд")
            ],
            [InlineKeyboardButton("сон", callback_data="act_сон")]
        ])

    @staticmethod
    def class_reactions(class_code: str) -> InlineKeyboardMarkup:
        opts = REACTIONS_BY_CLASS[class_code]
        buttons = [
            [InlineKeyboardButton(text, callback_data=f"class_{class_code}_{val}")]
            for text, val in opts
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def people_reactions():
        buttons = [
            [InlineKeyboardButton(f"{k+1}) {v}", callback_data=f"people_{k}")]
            for k, v in PEOPLE_REACTIONS.items()
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def item_reactions():
        buttons = [
            [InlineKeyboardButton(f"{(k+1) if k>=0 else 0}) {v}", callback_data=f"item_{k}")]
            for k, v in ITEM_REACTIONS.items()
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def building_class():
        buttons = [
            [InlineKeyboardButton(f"{code} – {desc}", callback_data=f"cls_{code}")]
            for code, desc in BUILDING_CLASSES.items()
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def damage_response_buttons(options):
        # options = [(text, callback_code), ...]
        buttons = []
        for i in range(0, len(options), 2):
            row = []
            for text, code in options[i:i+2]:
                row.append(InlineKeyboardButton(text, callback_data=code))
            buttons.append(row)
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def building_condition():
        buttons = []
        for text, code in BUILDING_CONDITIONS.items():
            buttons.append([InlineKeyboardButton(text, callback_data=f"cond_{code}")])
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def building_overall_state():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Устояло", callback_data="ov_1")],
            [InlineKeyboardButton("Значительно повреждено", callback_data="ov_4")],
            [InlineKeyboardButton("Полное обрушение", callback_data="ov_5")]
    ])

class Messages:
    DATE_PROMPT                = "📅 Укажите дату землетрясения (например: 2025-06-27):"
    TIME_PROMPT                = "⏰ Укажите примерное время землетрясения (например: 14:30):"
    ADDRESS_PROMPT             = "📍 Укажите адрес, где вы почувствовали землетрясение:"
    WELCOME                    = "🌍 Где вы находились во время землетрясения?"
    FLOOR_PROMPT               = "🏢 Укажите этаж и этажность здания (например: 3 5):"
    ACTIVITY_PROMPT            = "⚙️ Чем вы занимались в момент землетрясения?"
    PEOPLE_REACTION            = "🔍 Выберите вашу реакцию:"
    ITEM_REACTION              = "📌 Оцените реакцию предметов: {0} — {1}"
    BUILDING_CLASS_PROMPT      = "🏠 Выберите класс сейсмостойкости здания:"
    DAMAGE_CRACKS_PROMPT       = "🏚 Трещины в отделке, сопряжениях и стыках плит, дверных коробках, перегородках, карнизах, фронтонах, дымовых трубах?"
    DAMAGE_PLASTER_PROMPT      = "🏚 Откалывание кусков штукатурки?"
    DAMAGE_STRUCTURAL_PROMPT   = "🏚 Видимые повреждения конструктивных элементов (несущие стены и перекрытия)?"
    DAMAGE_OVERALL_PROMPT      = "🏚 Состояние здания в целом?"
    BUILDING_TECH_STATE_PROMPT = "🏗 Выберите техническое состояние здания до землетрясения:"
    FINAL_MESSAGE              = "📊 Спасибо за ответы!\nРасчетная интенсивность: {intensity:.1f} баллов"
    CANCEL                     = "Опрос отменен."
