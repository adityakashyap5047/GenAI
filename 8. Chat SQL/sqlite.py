import sqlite3

### Connect to SQLite3
connection = sqlite3.connect('student.db')

### Create a cursor object to interact with the database
cursor = connection.cursor()

