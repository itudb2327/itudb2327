from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, UserMixin,login_required,logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from login_register import login_page, register_page, validate_login,User
import mysql.connector
import suppliers
import customers
import purchases
import orders
from profiles import profile_page
from employee import Employees
from products import Products
import base64
import binascii
from io import BytesIO
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
        user_obj = User(id=user['id'], username=user['username'], password=user['password_hash'],status=user['status'], joined=user['joined'])
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
    
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 65 KB (BLOB)

@app.route('/')
def home():
    
    cursor=db.cursor()
    cursor.execute("""SELECT 
    suppliers.company,
    TotalProducts.ProductCount,
    purchase_orders.id,
    employees.first_name,
    employees.last_name
    FROM 
        suppliers
    JOIN (
        SELECT 
            products.supplier_ids,
            COUNT(*) AS ProductCount
        FROM 
            products
        GROUP BY 
            products.supplier_ids
    ) AS TotalProducts ON suppliers.id = TotalProducts.supplier_ids
    JOIN (
        SELECT 
            purchase_orders.supplier_id,
            purchase_orders.id,
            purchase_orders.created_by
        FROM 
            purchase_orders
        WHERE 
            purchase_orders.shipping_fee = (
                SELECT 
                    MAX(shipping_fee)
                FROM 
                    purchase_orders
            )
    ) AS purchase_orders ON suppliers.id = purchase_orders.supplier_id
    JOIN employees ON purchase_orders.created_by = employees.id;
    """)
    
                
    emp_of_month=cursor.fetchall()
    cursor.close()
    # print(row)
    product_id_list = Products.get_id_list(db)
    product_profit_list = Products.get_profit_list(db)
    return render_template('home.html',logged=current_user.is_authenticated,emp_of_month=emp_of_month, product_ids=product_id_list, profits=product_profit_list)

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
    return suppliers.index(db,current_user)
    
@app.route('/purchases',methods=("GET","POST"))
@login_required
def purchase():  
    if current_user.status=="admin":
        return purchases.index(db)    
    else:
        return render_template('unauthorized.html')
    
@app.route('/products',methods=("GET","POST"))
@login_required
def product():

    if request.method=="POST":
        # print(request.form)
        if "product_name" in request.form:
            return Products.add_product(db)
        elif "deleteId" in request.form:
            return Products.delete_product(db)
        elif "updateId" in request.form:
            return Products.update_product(db)
        elif "checkedCategory[]" in request.form:
            return Products.filter_product_by_category(db)
        elif "search" in request.form:
            return Products.search_product(db)
    else:
        category_list= Products.get_all_categories(db)
        product_list = Products.get_all_products(db)
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=product_list, category_list=category_list, company_list=company_list)

@app.route("/employees", methods=("GET","POST"))
@login_required
def employees_page():
    return Employees.index(db)
    

@app.route("/customers", methods=("GET","POST"))
def customers_page():
    form = customers.CustomerForm()
    # handle request by checking request methods and request types and call corresponding functions
    if request.method == 'POST':
        if 'deleteCustomerId' in request.form:
            return customers.delete(db, form)
        elif 'newCustomerId' in request.form:
            if form.validate_on_submit():
                return customers.new(db, form)
            else:
                # the 1 , 0 parameters indicate that the newCustomer form has not been validated
                return customers.index(db, form, 1, 0, "")
        elif 'updateCustomerId' in request.form:
            if form.validate_on_submit():
                return customers.update(db, form)
            else:
                 # the 0 , 1 parameters indicate that the updateCustomer form has not been validated
                return customers.index(db, form, 0, 1, request.form.get('updateCustomerId'))
        
    return customers.index(db, form, 0, 0, "")

@app.route("/orders", methods=("GET","POST"))
def orders_page():
    form = orders.OrdersForm()
    # fill options for the form
    form = orders.fillCustomerOptions(db, form)
    # handle request by checking request methods and request types and call corresponding functions
    if request.method == 'POST':
        if 'deleteOrderId' in request.form:
            return orders.delete(db, form)
        elif 'newOrderId' in request.form:
            if form.validate_on_submit():
                return orders.new(db, form)
            else:
                # the 1 , 0 parameters indicate that the newOrder form has not been validated
                return orders.index(db, form, 1, 0, "")
        elif 'updateOrderId' in request.form:
            if form.validate_on_submit():
                return orders.update(db, form)
            else:
                # the 0 , 1 parameters indicate that the updateOrder form has not been validated
                return orders.index(db, form, 0, 1, request.form.get('updateOrderId'))

    return orders.index(db, form, 0, 0, "")

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    cursor = db.cursor()
    audio_file = request.files['audio_file']
    audio_blob = audio_file.read()
    query = "UPDATE music SET audio_blob = (%s) WHERE id = 1"
    cursor.execute(query, (audio_blob,))
    db.commit()
    return home()

@app.route('/get_audio')
def get_audio():
    cursor = db.cursor()
    cursor.execute("SELECT audio_blob FROM music WHERE id = 1")
    audio_blob = cursor.fetchone()[0]
    if audio_blob:
        return send_file(BytesIO(audio_blob), mimetype='audio/mpeg', as_attachment=True, download_name='audio.mp3')
    else:
        return "Audio not found", 404

if __name__ == '__main__':
    app.run(debug=True)
