import mysql.connector
from flask import Flask, render_template, request, flash
import suppliers

class Products:
    def __init__(self, code, product_name, supplier_id, cost, list_price, quantity_per_unit, category) :
        self.code= code
        self.product_name =product_name
        
        self.supplier_id = supplier_id
        self.cost = cost
        self.list_price = list_price
        self.quantitiy_per_unit = quantity_per_unit
        self.category = category
        

    def get_all_products(db):
        cursor = db.cursor()
        product_list = []
        select_query=""" SELECT products.id, 
                        products.product_code, 
                        products.product_name, 
                        
                        products.supplier_ids, 
                        products.standard_cost, 
                        products.list_price, 
                        products.quantity_per_unit, 
                        products.category, 
                        suppliers.company FROM products INNER JOIN suppliers ON products.supplier_ids=suppliers.id"""
        cursor.execute(select_query)
        for id , product_code, name, supplier_id, cost, price, quan, category, supplier_company in cursor:
            product_list.append((supplier_company, id, Products(product_code,name, supplier_id, cost, price, quan, category)))
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
    def get_id_list(db):
        cursor = db.cursor()
        id_list = []
        select_query = """ SELECT product_name FROM products ORDER BY (list_price - standard_cost) desc LIMIT 5 """
        cursor.execute(select_query)
        for id in cursor:
            id_list.append(id)
        cursor.close()
        return id_list
    def get_profit_list(db):
        cursor = db.cursor()
        profit_list = []
        select_query = """ SELECT (list_price - standard_cost) FROM products ORDER BY (list_price - standard_cost) desc LIMIT 5 """
        cursor.execute(select_query)
        for profit in cursor:
            profit_list.append(profit)
        cursor.close()
        return profit_list
    
    def add_product(db):
        
        if(request.form['category']!=""):
            new_product = Products( request.form['product_code'],
                                request.form['product_name'],      
                                request.form['selected_supplier'],          
                                request.form['standard_cost'],
                                request.form['list_price'],
                                request.form['quantitiy_per_unit'],
                                request.form['category'])
            
            
        else : new_product = Products(  request.form['product_code'],
                                        request.form['product_name'],     
                                        request.form['selected_supplier'],          
                                        request.form['standard_cost'],
                                        request.form['list_price'],
                                        request.form['quantitiy_per_unit'],
                                        request.form['selected_category'])
        print("Form Data:")
        for key, value in request.form.items():
            print(f"{key}: {value}")
        cursor= db.cursor()
        query= """ INSERT INTO products (product_code, product_name , supplier_ids, standard_cost, list_price, quantity_per_unit, category)
          VALUES (%s, %s, %s, %s, %s, %s, %s) """
        
        values= (new_product.code, new_product.product_name, new_product.supplier_id, new_product.cost, new_product.list_price, new_product.quantitiy_per_unit, new_product.category)
        cursor.execute(query, values)
        db.commit()
        new_list = Products.get_all_products(db)
        category_list= Products.get_all_categories(db)
        
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=new_list, company_list=company_list, category_list=category_list )
        
    def delete_product(db):
        deletedproductId = request.form['deleteId']
        cursor = db.cursor()
        
        delete_query = f"DELETE FROM products WHERE id = '{deletedproductId}'"
        cursor.execute(delete_query)
        db.commit()
        new_list = Products.get_all_products(db)
        category_list= Products.get_all_categories(db)
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=new_list, company_list=company_list, category_list=category_list )
    def update_product( db):
        if("new_category" in request.form):
            updated_product = Products( request.form['new_product_code'],
                                request.form['new_product_name'],      
                                request.form['new_selected_supplier'],          
                                request.form['new_standard_cost'],
                                request.form['new_list_price'],
                                request.form['new_quantitiy_per_unit'],
                                request.form['new_category'])
            
            
        else : updated_product = Products(  request.form['new_product_code'],
                                        request.form['new_product_name'],     
                                        request.form['new_selected_supplier'],          
                                        request.form['new_standard_cost'],
                                        request.form['new_list_price'],
                                        request.form['new_quantitiy_per_unit'],
                                        request.form['new_selected_category'])
        
        cursor= db.cursor()

        print(request.form)
        print("category: " , updated_product.category)
        query= """ UPDATE products SET product_code = %s,
                                        product_name = %s,
                                        supplier_ids = %s,
                                        standard_cost = %s,
                                        list_price = %s,
                                        quantity_per_unit = %s,
                                        category = %s
                    WHERE id = %s """
        update_product_id = request.form['updateId']
        values= (updated_product.code, updated_product.product_name, updated_product.supplier_id, updated_product.cost, updated_product.list_price, updated_product.quantitiy_per_unit, updated_product.category, update_product_id)
        cursor.execute(query, values)
        db.commit()
        new_list = Products.get_all_products(db)
        category_list= Products.get_all_categories(db)
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=new_list, company_list=company_list, category_list=category_list )
    def filter_product_by_category(db):
        selected_categories = request.form.getlist('checkedCategory[]')
        all_products = Products.get_all_products(db)
        filtered_products = [product for product in all_products if product[2].category in selected_categories]
        category_list= Products.get_all_categories(db)
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=filtered_products, company_list=company_list, category_list=category_list )
    def search_product(db):
        product_list = Products.get_all_products(db)
        product_name =request.form['search']
        product_name = product_name.upper()
        filtered_product = []
        for company, product_id, product in product_list:
            if product_name in product.product_name.upper(): 
                filtered_product.append((company, product_id, product))
            elif product_name in product.code.upper():
                filtered_product.append((company, product_id, product))
        category_list= Products.get_all_categories(db)
        company_list= suppliers.get_supplier_company(db)
        return render_template("products.html", product_list=filtered_product, company_list=company_list, category_list=category_list)
