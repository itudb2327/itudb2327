import mysql.connector

db = mysql.connector.connect(
        host="northwind.cfl4fp0ymkxx.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="dh8zcJMSGQhlcHT554yX",
        database="northwind"
)

cursor = db.cursor()
