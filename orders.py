from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from flask import Flask, render_template, request, flash
from datetime import datetime

class Orders:
    def __init__(self, id, customer_name, order_date, ship_name, ship_address, ship_city, shipping_fee) :
        self.id = id
        self.customer_name = customer_name
        self.order_date = order_date
        self.ship_name = ship_name
        self.ship_address = ship_address
        self.ship_city = ship_city
        self.shipping_fee = shipping_fee

class OrdersForm(FlaskForm):
    orderCustomerName = SelectField('Customer Name', validators=[DataRequired(message= 'Customer name is required.')])
    orderOrderDate = DateTimeLocalField('Order Date',format='%Y-%m-%dT%H:%M', validators=[DataRequired(message = 'Order date is required.')])
    orderShipName = StringField('Ship Name')
    orderShipAddress = StringField('Ship Adress', validators=[Length(min=10, message='Address value must be 10 characters at minimum.')])
    orderShipCity = StringField('Ship City')
    orderShippingFee = DecimalField('Shipping Fee', validators=[NumberRange(max=300.00, message='Shipping fee can be 300.00 at maximum.')])  


def index(db, form, new_not_valid, update_not_valid, update_button_id):
    cursor = db.cursor()
    orders_list = []
    sort_by = request.args.get('sort_by')
    search_customer_name = request.args.get('search_customer_name')
    records = request.args.get('records')
    if sort_by or search_customer_name or records:
        db_query = handleFilters(sort_by, search_customer_name, records)
    else:
        db_query = """SELECT
                            orders.id,
                            CONCAT(customers.first_name, ' ', customers.last_name) AS customer_name,
                            orders.order_date,
                            orders.ship_name,
                            orders.ship_address,
                            orders.ship_city,
                            orders.shipping_fee
                        FROM
                            orders
                        JOIN
                            customers ON orders.customer_id = customers.id"""
    cursor.execute(db_query)
    for id, customer_name, order_date, ship_name, ship_address, ship_city, shipping_fee in cursor:
        orders_list.append(Orders( id, customer_name, order_date, ship_name, ship_address, ship_city, shipping_fee))
    cursor.close()
    return render_template("orders.html", orders_list = orders_list, form = form, new_not_valid = new_not_valid, update_not_valid = update_not_valid, update_button_id = update_button_id)

def handleFilters(sort_by, search_customer_name, records):
    if search_customer_name:
        db_query = f"""SELECT
                            orders.id,
                            CONCAT(customers.first_name, ' ', customers.last_name) AS customer_name,
                            orders.order_date,
                            orders.ship_name,
                            orders.ship_address,
                            orders.ship_city,
                            orders.shipping_fee
                        FROM
                            orders
                        JOIN
                            customers ON orders.customer_id = customers.id
                        WHERE 
                            LOWER(customer_name) = LOWER('{search_customer_name}') """
    else:
        db_query = """SELECT
                            orders.id,
                            CONCAT(customers.first_name, ' ', customers.last_name) AS customer_name,
                            orders.order_date,
                            orders.ship_name,
                            orders.ship_address,
                            orders.ship_city,
                            orders.shipping_fee
                        FROM
                            orders
                        JOIN
                            customers ON orders.customer_id = customers.id"""
        if sort_by:
            db_query += f" ORDER BY {sort_by}"
        if records:
            db_query +=  f" LIMIT {records}"
    return db_query

def delete(db, form):
    cursor = db.cursor()
    id = request.form.get('deleteOrderId')
    delete_query = f"DELETE FROM orders WHERE id = '{id}'"
    cursor.execute(delete_query)
    db.commit()
    return index(db, form, 0, 0, "")

def new(db, form):
    cursor = db.cursor()
    customer_id = request.form.get('orderCustomerName') 
    order_date = request.form.get('orderOrderDate')
    order_date = datetime.strptime(order_date, "%Y-%m-%dT%H:%M")
    order_date = datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S")
    ship_name = request.form.get('orderShipName')
    ship_address = request.form.get('orderShipAddress')
    ship_city = request.form.get('orderShipCity')
    shipping_fee = request.form.get('orderShippingFee')
    insert_query = f"INSERT INTO orders(customer_id, order_date, ship_name, ship_address, ship_city, shipping_fee) VALUES ({customer_id}, '{order_date}', '{ship_name}', '{ship_address}', '{ship_city}', {shipping_fee})"
    cursor.execute(insert_query)
    db.commit()
    return index(db, form, 0, 0, "")


def update(db, form):
    cursor = db.cursor()
    id = request.form.get('updateOrderId')
    customer_id = request.form.get('orderCustomerName') 
    order_date = request.form.get('orderOrderDate')
    order_date = datetime.strptime(order_date, "%Y-%m-%dT%H:%M")
    order_date = datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S")
    ship_name = request.form.get('orderShipName')
    ship_address = request.form.get('orderShipAddress')
    ship_city = request.form.get('orderShipCity')
    shipping_fee = request.form.get('orderShippingFee')
    update_query = f"UPDATE orders SET customer_id = {customer_id},order_date = '{order_date}', ship_name = '{ship_name}', ship_address = '{ship_address}', ship_city = '{ship_city}', shipping_fee = {shipping_fee} WHERE id = {id}"
    cursor.execute(update_query)
    db.commit()
    return index(db, form, 0, 0, "")

def fillCustomerOptions(db, form):
    cursor = db.cursor()
    query = "SELECT id, CONCAT(first_name, ' ', last_name) AS customer_name FROM customers"
    cursor.execute(query)
    form.orderCustomerName.choices = [(str(id), customer_name) for id, customer_name in cursor]
    return form


