import mysql.connector
from flask import Flask, render_template, request

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


def index(db):
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
    return render_template("customers.html", customers_list = customers_list)

