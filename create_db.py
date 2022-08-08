import sqlite3

connection = sqlite3.connect("app/database.db")

cursor = connection.cursor()

sql_file = open("schema.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)

print("The tables were created successfully!")