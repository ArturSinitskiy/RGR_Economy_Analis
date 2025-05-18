# database.py
import os
import sqlite3

# Определяем путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def create_database():
    """Создает базу данных и таблицу users в папке src/database/"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username: str, password: str) -> bool:
    """Добавляет пользователя в базу данных"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Пользователь уже существует
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_user(username: str, password: str) -> bool:
    """Проверяет существование пользователя"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                      (username, password))
        user = cursor.fetchone()
        return user is not None
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

# Создаем базу данных при импорте модуля
create_database()