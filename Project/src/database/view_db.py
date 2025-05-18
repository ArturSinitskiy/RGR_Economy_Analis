import sqlite3

import pandas as pd

# Подключаемся к базе
conn = sqlite3.connect("../database/users.db")

# Читаем таблицу 'users' в DataFrame
df = pd.read_sql_query("SELECT * FROM users", conn)

# Выводим аккуратную таблицу в консоль
print(df.to_markdown(tablefmt="grid"))  # Красивое отображение

# Закрываем соединение
conn.close()