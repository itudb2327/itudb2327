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
        if("first_name" in request.form):
            new_employee = Employees(request.form['first_name'], request.form['last_name'],request.form['job_title'],request.form['phone_number'], request.form['extra_notes'])
            
            Employees.add_employee(db,new_employee)
            new_list = Employees.get_all_employees(db)
            return render_template("employees.html", employee_list=new_list)
        elif("search" in request.form):
            employee_name =request.form['search']
            employee_name = employee_name.upper()
            filtered_employee_list = Employees.search_employee(employee_name, employee_list) 
            return render_template("employees.html", employee_list=filtered_employee_list)
     else:
        return render_template("employees.html", employee_list=employee_list)

@app.route("/customers", methods=("GET","POST"))
def customers_page():
    if request.method == 'POST':
        if 'deleteCustomerId' in request.form:
            return customers.delete(db)
        elif 'newCustomerId' in request.form:
            return customers.new(db)
        elif 'updateCustomerId' in request.form:
            return customers.update(db)
        
    return customers.index(db)

if __name__ == '__main__':
    app.run(debug=True)
