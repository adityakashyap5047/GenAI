import sqlite3

### Connect to SQLite3
connection = sqlite3.connect('student.db')

### Create a cursor object to interact with the database
cursor = connection.cursor()

### Create a table
table_info = """

    create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
                         SECTION VARCHAR(25), MARKS INT)

"""

cursor.execute(table_info)

### Insert data into the table
cursor.execute('''Insert Into STUDENT values('Krish', 'Data Science', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('John', 'Data Science', 'B', 100)''')
cursor.execute('''Insert Into STUDENT values('Sam', 'Data Science', 'C', 95)''')
cursor.execute('''Insert Into STUDENT values('Tom', 'DEVOPS', 'A', 85)''')
cursor.execute('''Insert Into STUDENT values('Jerry', 'DEVOPS', 'B', 80)''')


### Display all the records
print("The inserted records are:")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
