import mysql.connector
from flask import Flask, render_template, request,redirect,session,redirect
import re

class Purchase:
    def __init__(self, id=None, supplier_id=None, created_by=None, submitted_date=None,
                 creation_date=None, status_id=None, expected_date=None, shipping_fee=None,
                 taxes=None, payment_date=None, payment_method=None, notes=None,
                 approved_by=None, approved_date=None, submitted_by=None):
        
        self.id = id
        self.supplier_id = supplier_id
        self.created_by = created_by
        self.submitted_date = submitted_date
        self.creation_date = creation_date
        self.status_id = status_id
        self.expected_date = expected_date
        self.shipping_fee = shipping_fee
        self.taxes = taxes
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.notes = notes
        self.approved_by = approved_by
        self.approved_date = approved_date
        self.submitted_by = submitted_by


def return_record(cursor,active_filter):
    cursor.execute("""SELECT    purchase.id,
                                suppliers.company,
                                employees.last_name,
                                purchase.submitted_date,
                                purchase.creation_date,
                                purchase.status_id,
                                purchase.expected_date,
                                purchase.shipping_fee,
                                purchase.taxes,
                                purchase.payment_date,
                                purchase.payment_method,
                                purchase.notes,
                                purchase.approved_by,
                                purchase.approved_date,
                                purchase.submitted_by
                                FROM purchase_orders as purchase 
                                INNER JOIN suppliers ON purchase.supplier_id=suppliers.id 
                                INNER JOIN employees ON purchase.created_by=employees.id 
                                WHERE status_id=%s;""",(active_filter,))
    records = cursor.fetchall()  
    return records


def create_record(cursor, temp_purchase):
    statement = """
        INSERT INTO purchase_orders (
            supplier_id,
            created_by,
            submitted_date,
            creation_date,
            status_id,
            expected_date,
            shipping_fee,
            taxes,
            payment_date,
            payment_method,
            notes,
            approved_by,
            approved_date,
            submitted_by
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    values = (
        temp_purchase.supplier_id,
        temp_purchase.created_by,
        temp_purchase.submitted_date,
        temp_purchase.creation_date,
        temp_purchase.status_id,
        temp_purchase.expected_date,
        temp_purchase.shipping_fee,
        temp_purchase.taxes,
        temp_purchase.payment_date,
        temp_purchase.payment_method,
        temp_purchase.notes,
        temp_purchase.approved_by,
        temp_purchase.approved_date,
        temp_purchase.submitted_by
    )

    cursor.execute(statement, values)

    return redirect("purchases")

def get_all_purchases(db):
    cursor = db.cursor()
    purchase_list = []
    active_filter = session.get('active_filter')
    select_query = """SELECT id, supplier_id, created_by, submitted_date, 
                             creation_date, status_id, expected_date, shipping_fee, 
                             taxes, payment_date, payment_method, notes, 
                             approved_by, approved_date, submitted_by 
                      FROM purchase_orders WHERE status_id=%s"""
    cursor.execute(select_query,(active_filter,))
    results=cursor.fetchall()
    # print(results)
    for (
        purchase_id, supplier_id, created_by, submitted_date,
        creation_date, status_id, expected_date, shipping_fee,
        taxes, payment_date, payment_method, notes,
        approved_by, approved_date, submitted_by
    ) in results:
        purchase_list.append(
            Purchase(
                id=purchase_id,
                supplier_id=supplier_id,
                created_by=created_by,
                submitted_date=submitted_date,
                creation_date=creation_date,
                status_id=status_id,
                expected_date=expected_date,
                shipping_fee=shipping_fee,
                taxes=taxes,
                payment_date=payment_date,
                payment_method=payment_method,
                notes=notes,
                approved_by=approved_by,
                approved_date=approved_date,
                submitted_by=submitted_by
            )
        )

    cursor.close()
    return purchase_list,active_filter


def update_record(cursor, updateId, temp_purchase):
    statement = """
        UPDATE purchase_orders SET
            supplier_id=%s,
            created_by=%s,
            submitted_date=%s,
            creation_date=%s,
            status_id=%s,
            expected_date=%s,
            shipping_fee=%s,
            taxes=%s,
            payment_date=%s,
            payment_method=%s,
            notes=%s,
            approved_by=%s,
            approved_date=%s,
            submitted_by=%s
        WHERE ID=%s;
    """

    values = (
        temp_purchase.supplier_id,
        temp_purchase.created_by,
        temp_purchase.submitted_date,
        temp_purchase.creation_date,
        temp_purchase.status_id,
        temp_purchase.expected_date,
        temp_purchase.shipping_fee,
        temp_purchase.taxes,
        temp_purchase.payment_date,
        temp_purchase.payment_method,
        temp_purchase.notes,
        temp_purchase.approved_by,
        temp_purchase.approved_date,
        temp_purchase.submitted_by
    )
    
    

    cursor.execute(statement, list(values)+[updateId])
    
    return redirect("purchases")




def delete_record(cursor,updateId):
    statement ="DELETE FROM purchase_orders WHERE ID=%s;"   
    cursor.execute(statement, (updateId,))

def index(db):
    
    cursor = db.cursor()
    active_filter=-1
    records=[]
    # print(request.form.keys())
    if request.method =='POST':
        if 'querry' in request.form:
            search_for=request.form['search_for']
            querry =request.form['querry']
            records,active_filter=search_record(db,search_for,querry)
        if 'filter' in request.form:
            if 'filter' in request.form:
                filter = request.form["filter"]
                # Set the active_filter in the session
                session['active_filter'] = filter
            records = return_record(cursor,filter)  
        if 'operation' in request.form:
            operation=request.form["operation"]
            if operation == "0":  # add new record
                temp_purchase = Purchase(
                    supplier_id=request.form["supplier_id"],
                    created_by=request.form["created_by"],
                    submitted_date=request.form["submitted_date"],
                    creation_date=request.form["creation_date"],
                    status_id=request.form["status_id"],
                    expected_date=request.form["expected_date"],
                    shipping_fee=request.form["shipping_fee"],
                    taxes=request.form["taxes"],
                    payment_date=request.form["payment_date"],
                    payment_method=request.form["payment_method"],
                    notes=request.form["notes"],
                    approved_by=request.form["approved_by"],
                    approved_date=request.form["approved_date"],
                    submitted_by=request.form["submitted_by"]
                )

                create_record(cursor, temp_purchase)

            elif operation == "1":  # delete
                updateId = request.form["updateId"]
                delete_record(cursor, updateId)

            elif operation == "2":  # update
                temp_purchase = Purchase(
                    supplier_id=request.form["supplier_id"],
                    created_by=request.form["created_by"],
                    submitted_date=request.form["submitted_date"],
                    creation_date=request.form["creation_date"],
                    status_id=request.form["status_id"],
                    expected_date=request.form["expected_date"],
                    shipping_fee=request.form["shipping_fee"],
                    taxes=request.form["taxes"],
                    payment_date=request.form["payment_date"],
                    payment_method=request.form["payment_method"],
                    notes=request.form["notes"],
                    approved_by=request.form["approved_by"],
                    approved_date=request.form["approved_date"],
                    submitted_by=request.form["submitted_by"]
                )
                updateId = request.form["updateId"]
                update_record(cursor, updateId, temp_purchase)
            now = datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE TableLastUpdateInfo SET update_time=%s WHERE table_name='purchase_orders';",(formatted_time,))
            db.commit()#commit for all filters        
    update_time=display_last_update(cursor)
    
    return render_template('purchases.html',records=records,update_time=update_time,active_filter=active_filter)

def search_record(db,search_for,querry):
    
    purchase_list,active_filter = get_all_purchases(db)
    records=[]
    filtered_products=[]
    querry = querry.lower()
    filtered_list = []
    for purchase in purchase_list:
            
        searched_item = getattr(purchase, search_for, None)
        if re.findall(querry,str(searched_item)) :
            filtered_products.append(purchase)      
    for temp_purchase in filtered_products:
        
        record=(temp_purchase.id,
                temp_purchase.supplier_id,
                temp_purchase.created_by,
                temp_purchase.submitted_date,
                temp_purchase.creation_date,
                temp_purchase.status_id,
                temp_purchase.expected_date,
                temp_purchase.shipping_fee,
                temp_purchase.taxes,
                temp_purchase.payment_date,
                temp_purchase.payment_method,
                temp_purchase.notes,
                temp_purchase.approved_by,
                temp_purchase.approved_date,
                temp_purchase.submitted_by)
        records.append(record)
    
    for record in records:
        print(record[0],record[1])
    
    
    return records,active_filter


def display_last_update(cursor):
        cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='purchase_orders';")
        update_time=cursor.fetchall()
        update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone
        cursor.close()
        return update_time