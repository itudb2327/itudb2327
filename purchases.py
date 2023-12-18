import mysql.connector
from flask import Flask, render_template, request,redirect,session


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

from flask import redirect

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
    active_filter="-1"
    records=[]
    if request.method =='POST':
        print(request.form.keys())
        if 'filter' in request.form:
            filter=request.form["filter"]
            if filter == "0":#add new record
                active_filter="0"
                cursor.execute("SELECT * FROM purchase_orders WHERE status_id=0;")
                records = cursor.fetchall()    
            elif filter == "1":#add new record
                active_filter="1"
                cursor.execute("SELECT * FROM purchase_orders WHERE status_id=1;")
                records = cursor.fetchall()    
            elif filter == "2":#add new record
                active_filter="2"
                cursor.execute("SELECT * FROM purchase_orders WHERE status_id=2;")
                records = cursor.fetchall()    
            elif filter == "3":#add new record
                active_filter="3"
                cursor.execute("SELECT * FROM purchase_orders WHERE status_id=3;")
                records = cursor.fetchall()
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
    cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='purchase_orders';")
    update_time=cursor.fetchall()
    update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone
    cursor.close()

    return render_template('purchases.html',records=records,update_time=update_time,active_filter=active_filter)