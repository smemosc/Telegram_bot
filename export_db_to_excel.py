import sqlite3
import pandas as pd

def export_to_excel(db_path: str, excel_path: str):
    # 1) Подключаемся к SQLite
    conn = sqlite3.connect(db_path)

    # 2) Читаем всю таблицу users
    df_users = pd.read_sql_query("SELECT * FROM users", conn)

    # 3) Готовим DataFrame для отдельных реакций по предметам
    #    берём колонки user_id и RП0…RП5, "тащим" их в длинный формат
    rp_cols = [f"RП{i}" for i in range(6)]
    # если колонок нет (например, вы ещё не пересоздали БД) — пропустим
    existing = [c for c in rp_cols if c in df_users.columns]
    if existing:
        df_items = (
            df_users
            .loc[:, ["user_id"] + existing]
            .melt(id_vars="user_id", 
                  value_vars=existing,
                  var_name="item_class",
                  value_name="reaction")
            # преобразуем 'RП0' → 'П0'
            .assign(item_class=lambda d: d["item_class"].str.replace("RП", "П"))
            .dropna(subset=["reaction"])
        )
    else:
        df_items = pd.DataFrame(columns=["user_id","item_class","reaction"])

    # 4) Записываем оба листа в один .xlsx
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_users.to_excel(writer, sheet_name='users', index=False)
        df_items.to_excel(writer, sheet_name='item_reactions', index=False)

    conn.close()
    print(f"Экспорт завершён: {excel_path}")

if __name__ == "__main__":
    export_to_excel('bot.db', 'bot_export.xlsx')
