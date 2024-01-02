import mysql.connector
from flask import Flask, render_template, request,redirect,session,redirect
import re
from employee import Employees
from datetime import datetime, timedelta
# Define the 'Purchase' class to represent purchase order objects
class Purchase:
    # Constructor to initialize attributes
    def __init__(self, id=None, supplier_id=None, created_by=None, submitted_date=None,
                 creation_date=None, status_id=None, expected_date=None, shipping_fee=None,
                 taxes=None, payment_date=None, payment_method=None, notes=None,
                 approved_by=None, approved_date=None, submitted_by=None):
        # Initialize attributes with provided values
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

# Function to retrieve a list of all employees from the database
def get_all_employees(db):
    # Create a cursor for database operations
    cursor = db.cursor()
    employee_list = []
     # Execute SQL query 
    select_query=" SELECT id,last_name FROM employees ;"
    cursor.execute(select_query)
    # Fetch results and append to the 'employee_list'
    for id, last_name in cursor:
        employee_list.append((id,last_name))
    cursor.close()
    return employee_list
# Function to retrieve a list of all suppliers from the database
def get_all_suppliers(db):
     # Create a cursor for database operations
    cursor = db.cursor()
    supplier_list = []
    # Execute SQL query to select supplier IDs and company names
    select_query=" SELECT id,company FROM suppliers ;"
    cursor.execute(select_query)
    # Fetch results and append to the 'supplier_list'
    for id, last_name in cursor:
        supplier_list.append((id,last_name))
    cursor.close()
    return supplier_list
# Function to retrieve purchase order records based on a specified status
def return_record(cursor,active_filter):
     # Execute SQL query to select purchase order information with joins
    cursor.execute("""SELECT    purchase.id,
                                suppliers.company,
                                creator.last_name,
                                purchase.submitted_date,
                                purchase.creation_date,
                                purchase.status_id,
                                purchase.expected_date,
                                purchase.shipping_fee,
                                purchase.taxes,
                                purchase.payment_date,
                                purchase.payment_method,
                                purchase.notes,
                                approver.last_name,
                                purchase.approved_date,
                                submitter.last_name
                                FROM purchase_orders as purchase 
                                INNER JOIN suppliers ON purchase.supplier_id=suppliers.id 
                                INNER JOIN employees AS creator ON purchase.created_by=creator.id
                                INNER JOIN employees AS approver ON purchase.approved_by=approver.id 
                                INNER JOIN employees AS submitter ON purchase.submitted_by=submitter.id 
                                WHERE status_id=%s;""",(active_filter,))
    records = []
    # Fetch results and create 'Purchase' objects to append to 'records'
    for row in cursor.fetchall():
        purchase = Purchase(
            id=row[0],
            supplier_id=row[1],
            created_by=row[2],
            submitted_date=row[3],
            creation_date=row[4],
            status_id=row[5],
            expected_date=row[6],
            shipping_fee=row[7],
            taxes=row[8],
            payment_date=row[9],
            payment_method=row[10],
            notes=row[11],
            approved_by=row[12],
            approved_date=row[13],
            submitted_by=row[14]
        )
        records.append(purchase)
    # print(records)    
    return records

# Function to create a new purchase order record in the database
def create_record(cursor, temp_purchase):
 # SQL statement to insert a new record into the 'purchase_orders' table
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
# Function to retrieve all purchase orders from the database
def get_all_purchases(db):
    cursor = db.cursor()
    active_filter = session.get('active_filter')
    results=return_record(cursor,active_filter)
   

    cursor.close()
    return results,active_filter

# Function to update an existing purchase order record in the database
def update_record(cursor, updateId, temp_purchase):
    # SQL statement to update a record in the 'purchase_orders' table
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



# Function to delete a purchase order record from the database
def delete_record(cursor,updateId):
    statement ="DELETE FROM purchase_orders WHERE ID=%s;"   
    cursor.execute(statement, (updateId,))
    
# Main function to handle requests and render the purchase orders page
def index(db):
    
    cursor = db.cursor()
    active_filter=-1
    records=[]
    # print(operation)
    print(request.form.keys())
     # Check for form submission and perform corresponding actions
    if request.method =='POST':
        # Check for a search query in the form
        if 'querry' in request.form:
            search_for=request.form['search_for']
            querry =request.form['querry']
            records,active_filter=search_record(db,search_for,querry)
        # Check for a filter selection in the form    
        if 'filter' in request.form:
            if 'filter' in request.form:
                filter = request.form["filter"]
                # Set the active_filter in the session
                session['active_filter'] = filter
            records = return_record(cursor,filter)
        # Check for an operation (add, delete, update) in the form
        if 'operation' in request.form:
            operation=request.form["operation"]
            # print(operation)
             # Perform corresponding operation based on the operation value
            if operation == "0":  # add new record
                temp_purchase = Purchase(
                    supplier_id=request.form["supplier_id"] if request.form["supplier_id"] else None,
                    created_by=request.form["created_by"] if request.form["created_by"] else None,
                    submitted_date=request.form["submitted_date"] if request.form["submitted_date"] else None,
                    creation_date=request.form["creation_date"] if request.form["creation_date"] else None,
                    status_id=request.form["status_id"] if request.form["status_id"] else None,
                    expected_date=request.form["expected_date"] if request.form["expected_date"] else None,
                    shipping_fee=request.form["shipping_fee"] if request.form["shipping_fee"] else None,
                    taxes=request.form["taxes"] if request.form["taxes"] else None,
                    payment_date=request.form["payment_date"] if request.form["payment_date"] else None,
                    payment_method=request.form["payment_method"] if request.form["payment_method"] else None,
                    notes=request.form["notes"] if request.form["notes"] else None,
                    approved_by=request.form["approved_by"] if request.form["approved_by"] else None,
                    approved_date=request.form["approved_date"] if request.form["approved_date"] else None,
                    submitted_by=request.form["submitted_by"] if request.form["submitted_by"] else None
                )
                # Call the create_record function to add a new record
                create_record(cursor, temp_purchase)

            elif operation == "1":  # delete
                updateId = request.form["updateIdHidden_conf"]
                # Call the delete_record function to delete a record
                delete_record(cursor, updateId)

            elif operation == "2":  # update
                temp_purchase = Purchase(
                    supplier_id=request.form["u_supplier_id"],
                    created_by=request.form["u_created_by"],
                    submitted_date=request.form["u_submitted_date"],
                    creation_date=request.form["u_creation_date"],
                    status_id=request.form["u_status_id"],
                    expected_date=request.form["u_expected_date"],
                    shipping_fee=request.form["u_shipping_fee"],
                    taxes=request.form["u_taxes"],
                    payment_date=request.form["u_payment_date"],
                    payment_method=request.form["u_payment_method"],
                    notes=request.form["u_notes"],
                    approved_by=request.form["u_approved_by"],
                    approved_date=request.form["u_approved_date"],
                    submitted_by=request.form["u_submitted_by"]
                )
                updateId = request.form["updateIdHidden"]
                # Call the update_record function to update a record
                update_record(cursor, updateId, temp_purchase)
            # Get the current timestamp    
            now = datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # Update the last update time in the database
            cursor.execute("UPDATE TableLastUpdateInfo SET update_time=%s WHERE table_name='purchase_orders';",(formatted_time,))
            # Commit the changes to the database
            db.commit()#commit for all filters  
    # Retrieve the last update time for display
    update_time=display_last_update(cursor)
    # Retrieve the list of suppliers and employees for dropdowns
    suppliers=get_all_suppliers(db)

    employees=get_all_employees(db)
   
    
    cursor.close()
    # Retrieve the active filter from the session
    if 'active_filter' is session.keys():
        active_filter=session['active_filter'] 
    # print(employees)
    # Render the 'purchases.html' template with the necessary data
    return render_template('purchases.html',records=records,update_time=update_time,active_filter=active_filter,suppliers=suppliers,employees=employees)
# Function to search for purchase order records based on a query
def search_record(db,search_for,querry):
    
    purchase_list,active_filter = get_all_purchases(db)
    print(purchase_list)
    filtered_products=[]
    querry = querry.lower()
    filtered_list = []
    # Iterate through purchase orders and filter based on the query 
    for purchase in purchase_list:
            
        searched_item = getattr(purchase, search_for, None)
        searched_item=str(searched_item).lower()
        # print(searched_item)
        # print(querry)
        if re.findall(querry,str(searched_item)) :
            # print("asd")
            filtered_products.append(purchase)      
    
    
    
    return filtered_products,active_filter

# Function to display the last update time for the purchase orders table
def display_last_update(cursor):
        cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='purchase_orders';")
        update_time=cursor.fetchall()
        update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone
        # cursor.close()
        return update_time