# data_manager.py
import sqlite3
from typing import Dict

import pandas as pd


class FinancialDataManager:
	def __init__(self, db_path: str = "financial_data.db"):
		self.db_path = db_path
		self._init_db()

	def _init_db(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()

		# Создаем таблицу для хранения данных
		cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter_name TEXT NOT NULL,
            parameter_code TEXT NOT NULL,
            year_2013 REAL,
            year_2014 REAL,
            year_2015 REAL,
            unpaid_capital REAL,
            own_shares REAL,
            reserve_capital_1 REAL,
            reserve_capital_2 REAL,
            reserve_capital_3 REAL,
            additional_capital_1 REAL,
            additional_capital_2 REAL,
            additional_capital_3 REAL,
            retained_earnings_1 REAL,
            retained_earnings_2 REAL,
            retained_earnings_3 REAL,
            net_profit REAL,
            total REAL
        )
        """)
		conn.commit()
		conn.close()

	def load_data_from_excel(self, file_path: str):
		"""Загрузка данных из Excel в базу данных"""

	# Здесь будет код для парсинга вашего Excel файла
	# и загрузки данных в SQLite

	def get_data_for_years(self, main_year: int) -> Dict:
		"""Получение данных для выбранного года и предыдущего"""
		conn = sqlite3.connect(self.db_path)

		if main_year == 2013:
			# Для 2013 года нет предыдущего года данных
			query = """
            SELECT parameter_name, parameter_code, 
                   year_2013 as main_year, 
                   NULL as previous_year
            FROM financial_data
            """
		elif main_year == 2014:
			query = """
            SELECT parameter_name, parameter_code, 
                   year_2014 as main_year, 
                   year_2013 as previous_year
            FROM financial_data
            """
		elif main_year == 2015:
			query = """
            SELECT parameter_name, parameter_code, 
                   year_2015 as main_year, 
                   year_2014 as previous_year
            FROM financial_data
            """

		df = pd.read_sql_query(query, conn)
		conn.close()

		# Рассчитываем дополнительные показатели
		df['growth_rate'] = (df['main_year'] / df['previous_year']) * 100
		df['absolute_change'] = df['main_year'] - df['previous_year']

		return df.to_dict('records')