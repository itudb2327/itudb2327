from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, UserMixin,login_required,logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from login_register import login_page, register_page, validate_login
import mysql.connector
import suppliers
import customers
import orders
from employee import Employees
app = Flask(__name__)
app.secret_key = 'MongoDB'

login_manager = LoginManager(app)

db = mysql.connector.connect(
    host="northwind.cfl4fp0ymkxx.eu-north-1.rds.amazonaws.com",
    user="admin",
    password="dh8zcJMSGQhlcHT554yX",
    database="northwind"
)
@login_manager.user_loader
def load_user(user_id):
    # Assuming your 'users' table has an 'id' column
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if user:
        user_obj = UserMixin()
        user_obj.id = user['id']
        return user_obj
    return None
    
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))  # Redirect to the home page after logout
    


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_page(db)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_page(db)
    
@app.route('/suppliers',methods=("GET","POST"))
@login_required
def supplier():
    return suppliers.index(db)
    
@app.route('/orders',methods=("GET","POST"))
@login_required
def order():
    return orders.index(db)    
    
@app.route("/employees", methods=("GET","POST"))
#@login_required
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
        elif("deleteId" in request.form):
            deletedEmployeeId = request.form['deleteId']
            print("Id: ", deletedEmployeeId)
            Employees.delete_employee(db, deletedEmployeeId)
            new_list = Employees.get_all_employees(db)
            return render_template("employees.html", employee_list=new_list)
     else:
        return render_template("employees.html", employee_list=employee_list)


@app.route("/customers", methods=("GET","POST"))
@login_required
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
