import sqlite3
import logging
from contextlib import contextmanager
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)
DB_NAME = 'bot.db'
DB_TIMEOUT = 30  # seconds

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Инициализация структуры БД с полной схемой для реакций предметов"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Удаляем старую таблицу
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Создаем новую таблицу с полным набором полей
        cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            
            -- Временные метки и локация
            quake_datetime TEXT,  -- Формат: "YYYY-MM-DD HH:MM"
            location TEXT,        -- Чистый адрес
            floor INTEGER,         -- Этаж
            building_floors INTEGER, -- Этажность здания
            
            -- Реакции человека
            people_class TEXT,     -- Класс человека (Л0-Л5/2)
            RЛ0 REAL,              -- Реакция класса Л0
            RЛ1 REAL,              -- Реакция класса Л1
            RЛ2 REAL,
            RЛ3 REAL,
            RЛ4 REAL,
            RЛ5 REAL,
            I_Л REAL,              -- Интенсивность для человека
            W_Л REAL,              -- Вес реакции человека
            free_people_reaction TEXT, -- Произвольное описание
            
            -- Реакции предметов (полный набор для каждого класса)
            RП0 INTEGER,           -- Реакция предметов П0
            IП0 REAL,              -- Интенсивность для П0
            WП0 REAL,              -- Вес для П0
            RП1 INTEGER,
            IП1 REAL,
            WП1 REAL,
            RП2 INTEGER,
            IП2 REAL,
            WП2 REAL,
            RП3 INTEGER,
            IП3 REAL,
            WП3 REAL,
            RП4 INTEGER,
            IП4 REAL,
            WП4 REAL,
            RП5 INTEGER,
            IП5 REAL,
            WП5 REAL,
            
            -- Средние значения по предметам
            RП REAL,               -- Средневзвешенная реакция (∑(RПx*WПx)/∑WПx)
            IП REAL,               -- Средневзвешенная интенсивность (∑(IПx*WПx)/∑WПx)
            
            -- Параметры здания
            C0 INTEGER,            -- Класс здания
            C1 REAL,               -- Техсостояние
            C2 REAL,               -- Возрастной коэффициент
            C3 REAL,               -- Коэф. формы
            C4 REAL,               -- Коэф. этажности
            C_total REAL,          -- Итоговый класс
            RC INTEGER,            -- Максимальный ущерб
            I_С REAL,              -- Интенсивность для здания
            W_С REAL,              -- Вес для здания
            free_building_damage TEXT, -- Описание повреждений
            
            -- Итоговые значения
            intensity REAL,        -- Расчетная интенсивность
            
            -- Технические метки
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Оптимизируем запросы по user_id
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_user_id 
        ON users(user_id)
        ''')
        
        # Индекс для анализа данных по времени
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_quake_datetime 
        ON users(quake_datetime)
        ''')
        
        conn.commit()

def save_data(user_id: int, **kwargs: Any) -> bool:
    """
    Обновленная функция сохранения с поддержкой quake_datetime
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if kwargs:
                # Проверяем существование записи
                cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
                exists = cursor.fetchone() is not None

                cols = list(kwargs.keys())
                vals = list(kwargs.values())

                if exists:
                    set_clause = ", ".join(f"{c} = ?" for c in cols)
                    sql = f"""
                        UPDATE users 
                        SET {set_clause}, updated_at = CURRENT_TIMESTAMP 
                        WHERE user_id = ?
                    """
                    cursor.execute(sql, vals + [user_id])
                else:
                    columns = ["user_id"] + cols
                    placeholders = ["?"] * (1 + len(cols))
                    sql = f"""
                        INSERT INTO users ({', '.join(columns)}) 
                        VALUES ({', '.join(placeholders)})
                    """
                    cursor.execute(sql, [user_id] + vals)

            conn.commit()
            return True

    except sqlite3.Error as e:
        logger.error(f"Error saving data for user {user_id}: {e}")
        return False

def get_user_data(user_id: int, field: str) -> Optional[Any]:
    """Чтение данных из нового формата таблицы"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {field} FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return row[field] if row else None
    except sqlite3.Error as e:
        logger.error(f"Error getting '{field}' for user {user_id}: {e}")
        return None

def get_all_user_data(user_id: int) -> Optional[Dict[str, Any]]:
    """Получение всех данных пользователя"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        logger.error(f"Error getting all data for user {user_id}: {e}")
        return None