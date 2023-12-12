from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import Flask, render_template, request, flash

class Customer:
    def __init__(self, id, company, last_name, first_name, job_title, business_phone, address, city) :
        self.id = id
        self.company = company
        self.last_name = last_name
        self.first_name = first_name
        self.job_title = job_title
        self.business_phone = business_phone
        self.address = address
        self.city = city

class CustomerForm(FlaskForm):
    customerCompany = StringField('Company', validators=[DataRequired(message= 'Company is required.')])
    customerFirstName = StringField('First Name', validators=[DataRequired(message = 'First name is required.')])
    customerLastName = StringField('Last Name', validators=[DataRequired(message = 'Last name is required.')])
    customerJobTitle = StringField('Job Title')
    customerBussinessPhone = StringField('Business Phone', validators=[Length(min=13, max=13, message="Business phone must be in the format: (123)555-0100")])
    customerAddress = StringField('Address', validators=[Length(min=10, message='Address value must be 10 characters at minimum.')])
    customerCity = StringField('City')


def index(db, form):
    cursor = db.cursor()
    customers_list = []
    sort_by = request.args.get('sort_by')
    if sort_by:
        db_query = f"SELECT id, company, last_name, first_name, job_title, business_phone, address, city FROM customers ORDER BY {sort_by}"
    else:
        db_query = "SELECT id, company, last_name, first_name, job_title, business_phone, address, city FROM customers"
    cursor.execute(db_query)
    for id, company, last_name, first_name, job_title, business_phone, address, city in cursor:
        customers_list.append(Customer(id, company, last_name, first_name, job_title, business_phone, address, city))
    cursor.close()
    return render_template("customers.html", customers_list = customers_list, form = form)

def delete(db, form):
    cursor = db.cursor()
    id = request.form.get('deleteCustomerId')
    delete_query = f"DELETE FROM customers WHERE id = '{id}'"
    cursor.execute(delete_query)
    db.commit()
    flash('Customer deleted successfully', 'success')
    return index(db, form)

def new(db, form):
    cursor = db.cursor()
    company = request.form.get('customerCompany')
    first_name = request.form.get('customerFirstName')
    last_name = request.form.get('customerLastName')
    job_title = request.form.get('customerJobTitle')
    business_phone = request.form.get('customerBussinessPhone')
    address = request.form.get('customerAddress')
    city = request.form.get('customerCity')
    insert_query = f"INSERT INTO customers(company, last_name, first_name, job_title, business_phone, address, city) VALUES ('{company}', '{last_name}', '{first_name}', '{job_title}', '{business_phone}', '{address}', '{city}')"
    cursor.execute(insert_query)
    db.commit()
    return index(db, form)


def update(db, form):
    cursor = db.cursor()
    id = request.form.get('updateCustomerId')
    company = request.form.get('customerCompany')
    first_name = request.form.get('customerFirstName')
    last_name = request.form.get('customerLastName')
    job_title = request.form.get('customerJobTitle')
    business_phone = request.form.get('customerBussinessPhone')
    address = request.form.get('customerAddress')
    city = request.form.get('customerCity')
    update_query = f"UPDATE customers SET company = '{company}',last_name = '{last_name}', first_name = '{first_name}', job_title = '{job_title}', business_phone = '{business_phone}', address = '{address}', city = '{city}' WHERE id = {id}"
    cursor.execute(update_query)
    db.commit()
    return index(db, form)

