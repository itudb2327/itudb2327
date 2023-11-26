import mysql.connector
from flask import Flask, render_template,url_for,request
from employee import Employees
import customers
import suppliers
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

@app.route('/suppliers',methods=("GET","POST"))
def supplier():
    return suppliers.index(db)
    
@app.route("/employees", methods=("GET","POST"))
def employees_page():
     employee_list=Employees.get_all_employees(db)
     if request.method == "POST":
        employee_name =request.form['search']
        employee_name = employee_name.upper()
        filtered_employee_list = Employees.search_employee(employee_name, employee_list) 
        return render_template("employees.html", employee_list=filtered_employee_list)
     else:
        return render_template("employees.html", employee_list=employee_list)

@app.route("/customers", methods=("GET","POST"))
def customers_page():
    return customers.index(db)

@app.route("/delete_customer/<int:customer_id>", methods=("GET", "POST"))
def delete_customer(customer_id):
    return customers.delete(db, customer_id)
if __name__ == '__main__':
    app.run(debug=True)
