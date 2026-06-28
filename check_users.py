import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

print("Total users:", len(users))

for user in users:
    print(user)

connection.close()