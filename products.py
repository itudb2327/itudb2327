import mysql.connector
from flask import Flask, render_template, request, flash

class Products:
    def __init__(self, code, product_name, description, supplier_id, cost, list_price, quantity_per_unit, category) :
        self.code= code
        self.product_name =product_name
        self.job_title = description
        self.supplier_id = supplier_id
        self.cost = cost
        self.list_price = list_price
        self.quantitiy_per_unit = quantity_per_unit
        self.category = category

    def get_all_products(db):
        cursor = db.cursor()
        product_list = []
        select_query=""" SELECT id, product_code, product_name, description, supplier_ids, standard_cost, list_price, quantity_per_unit, category FROM products """
        cursor.execute(select_query)
        for id , product_code, name, description, supplier_id, cost, price, quan, category in cursor:
            product_list.append((id, Products(product_code,name, description, supplier_id, cost, price, quan, category)))
        cursor.close()
        return product_list
    
    def get_all_categories(db):
        cursor = db.cursor()
        category_list = []
        select_query = """ SELECT DISTINCT category FROM products """
        cursor.execute(select_query)
        for category in cursor:
            category_list.append(category)
        cursor.close()
        return category_list