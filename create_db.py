import mysql.connector

my = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password123",
)

my_cursor = my.cursor()

my_cursor.execute("CREATE DATABASE sportnews_app")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)