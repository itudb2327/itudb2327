import mysql.connector
from flask import Flask, render_template

db = mysql.connector.connect(
    host="northwind.cfl4fp0ymkxx.eu-north-1.rds.amazonaws.com",
    user="admin",
    password="dh8zcJMSGQhlcHT554yX",
    database="northwind"
)

app = Flask(__name__)

@app.route('/')
def home():
     return render_template('base.html',)

@app.route('/suppliers')
def supplier():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()

    cursor.close()

    
    db.close()

    return render_template('suppliers.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
