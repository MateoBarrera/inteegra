import pandas as pd
from unittest import TestCase
from app.database import *


class TestSQLConnector(TestCase):
    def test_connection(self):
        sql_manager = SQLConnector()
        self.assertIsNotNone(sql_manager.get_engine())

    def test_update_from_admin(self):
        sql_manager = SQLConnector()
        data = pd.read_excel('test/data/Users.xlsx', engine='openpyxl').to_dict(orient='records')
        result = sql_manager.update_from_admin('users', data)
        self.assertIsNotNone(sql_manager.get_engine())
