import mysql.connector
from flask import Flask, render_template,url_for,request
from supplier import Supplier
from employee import Employees
import customers

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
    if request.method =='POST':
        temp_supplier=Supplier()
        temp_supplier.company=request.form["company"]
        temp_supplier.business_phone=request.form["business_phone"]
        temp_supplier.address=request.form["address"]
        temp_supplier.city=request.form["city"]
        temp_supplier.country_region=request.form["country_region"]
        temp_supplier.email_address=request.form["email_address"]
        temp_supplier.fax_number=request.form["fax_number"]
        temp_supplier.first_name=request.form["first_name"]
        temp_supplier.last_name=request.form["last_name"]
        temp_supplier.state_province=request.form["state_province"]
        temp_supplier.web_page=request.form["web_page"]
        temp_supplier.job_title=request.form["job_title"]
        temp_supplier.home_phone=request.form["home_phone"]
        temp_supplier.zip_postal_code=request.form["zip_postal_code"]
        print(temp_supplier)
        pass
    else:
        pass
    cursor = db.cursor()
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()
    cursor.close()
    

    return render_template('suppliers.html', records=records)


@app.route("/employees")
def employees_page():
     cursor = db.cursor()
     employee_list = []
     select_query=" SELECT id, first_name, last_name, job_title, business_phone, notes FROM employees "
     cursor.execute(select_query)
     for employee_id, first_name, last_name, job_title, business_phone, notes in cursor:
        employee_list.append((employee_id, Employees(first_name,last_name, job_title, business_phone, notes)))
     cursor.close()
     return render_template("employees.html", employee_list=employee_list)

@app.route("/customers")
def customers_page():
    return customers.index(db)

if __name__ == '__main__':
    app.run(debug=True)
