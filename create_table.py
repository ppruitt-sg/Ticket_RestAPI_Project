import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS customers (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                email text,\
                name text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS employees (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                email text,\
                name text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS tickets (\
                    number INTEGER PRIMARY KEY AUTOINCREMENT,\
                    customer_id int,\
                    employee_id int, \
                    subject text, \
                    FOREIGN KEY(customer_id) REFERENCES customers (id),\
                    FOREIGN KEY(employee_id) REFERENCES employees (id))"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS comments (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    number int,\
                    timestamp int,\
                    from_email text,\
                    content text,\
                    FOREIGN KEY (number) REFERENCES\
                    tickets(number) ON DELETE CASCADE)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS auth (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    username text,\
                    password text)"
cursor.execute(create_table)

connection.commit()

connection.close()
