from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, UserMixin,login_required,logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from login_register import login_page, register_page, validate_login,User
import mysql.connector
import suppliers
import customers
import orders
from profile import profile_page
from employee import Employees
import base64
import binascii
app = Flask(__name__)
app.secret_key = 'MongoDB'

login_manager = LoginManager(app)

db = mysql.connector.connect(
    host="northwind.cfl4fp0ymkxx.eu-north-1.rds.amazonaws.com",
    user="admin",
    password="z2dz8C0kIuN3EZqEoi82",
    database="northwind"
)



@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if user:
        user_obj = User(id=user['id'], username=user['username'], password=user['password_hash'],status=user['status'], joined=user['joined'],profile_picture=['profile_picture'])
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
    # cursor = db.cursor()
    # cursor.execute("select * from TableLastUpdateInfo;")
    # cursor.execute("CREATE TABLE TableLastUpdateInfo (table_name VARCHAR(255) NOT NULL,update_time TIMESTAMP NOT NULL,PRIMARY KEY (table_name));")
    # cursor.execute("INSERT INTO TableLastUpdateInfo (table_name,update_time)VALUES ('suppliers',NOW());")
    # asd=cursor.fetchall()
    # print(asd)
    # cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) NOT NULL UNIQUE,password_hash VARCHAR(100) NOT NULL,status VARCHAR(20) NOT NULL default 'user',joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP, profile_picture BLOB);")
    # db.commit()
   
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_page(db)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_page(db)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    return profile_page(db,current_user)    
    
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
#@login_required
def customers_page():
    form = customers.CustomerForm()
    if request.method == 'POST' and form.validate_on_submit():
        if 'deleteCustomerId' in request.form:
            return customers.delete(db, form)
        elif 'newCustomerId' in request.form:
            return customers.new(db, form)
        elif 'updateCustomerId' in request.form:
            return customers.update(db, form)
        
    return customers.index(db, form)

if __name__ == '__main__':
    app.run(debug=True)
