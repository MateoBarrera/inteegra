"""Test file for ORM implementation of SQLAlchemy

Didn't associate to the main project's files.

@Author: Mateo Barrera

@Date: 02-04-2022
"""
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, Text, String
from sqlalchemy.sql import select


""" engine = create_engine('sqlite:///sqlite/NewDB.db')
connection = engine.connect() """
# result = engine.execute("select * from users")
""" result = engine.execute(emission_table.select())
for row in result:
    print(row)
result.close() """

# Insert ####
""" ins = users_table.insert().values(id_login='1', name='Jack Jones', organization='Univalle')
result = engine.execute(ins) """
# Select ####
""" sel = select(iaad_table)
result = engine.execute(sel)
columns = [col for col in result.keys()]
rows = [dict(zip(columns, row)) for row in result.fetchall()]
print(rows) """
