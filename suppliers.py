import mysql.connector
from flask import Flask, render_template, request,redirect,session
import time
from datetime import datetime, timedelta
class Supplier:
    def __init__(self, id=None, company=None, last_name=None, first_name=None, email_address=None, job_title=None,
                 business_phone=None, home_phone=None, mobile_phone=None, fax_number=None, address=None,
                 city=None, state_province=None, zip_postal_code=None, country_region=None, web_page=None,
                 notes=None, attachments=None):
        self.id = id
        self.company = company
        self.last_name = last_name
        self.first_name = first_name
        self.email_address = email_address
        self.job_title = job_title
        self.business_phone = business_phone
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.fax_number = fax_number
        self.address = address
        self.city = city
        self.state_province = state_province
        self.zip_postal_code = zip_postal_code
        self.country_region = country_region
        self.web_page = web_page
        self.notes = notes
        self.attachments = attachments
            
        

def create_record(cursor,temp_supplier):
    

    statement = """
        INSERT INTO suppliers (
            company,
            last_name,
            first_name,
            email_address,
            job_title,
            home_phone,
            business_phone,
            mobile_phone,
            fax_number,
            address,
            city,
            state_province,
            zip_postal_code,
            country_region,
            web_page,
            notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
      """

    
    values = (
        temp_supplier.company,
        temp_supplier.last_name,
        temp_supplier.first_name,
        temp_supplier.email_address,
        temp_supplier.job_title,
        temp_supplier.home_phone,
        temp_supplier.business_phone,
        temp_supplier.mobile_phone,
        temp_supplier.fax_number,
        temp_supplier.address,
        temp_supplier.city,
        temp_supplier.state_province,
        temp_supplier.zip_postal_code,
        temp_supplier.country_region,
        temp_supplier.web_page,
        temp_supplier.notes
    )   
    cursor.execute(statement, values)

    return redirect("suppliers")
    
def update_record(cursor,updateId,temp_supplier):
    statement = """
        UPDATE suppliers SET
            company=%s,
            last_name=%s,
            first_name=%s,
            email_address=%s,
            job_title=%s,
            home_phone=%s,
            business_phone=%s,
            mobile_phone=%s,
            fax_number=%s,
            address=%s,
            city=%s,
            state_province=%s,
            zip_postal_code=%s,
            country_region=%s,
            web_page=%s,
            notes=%s

        WHERE ID=%s;
      """

    
    values = (
        temp_supplier.company,
        temp_supplier.last_name,
        temp_supplier.first_name,
        temp_supplier.email_address,
        temp_supplier.job_title,
        temp_supplier.home_phone,
        temp_supplier.business_phone,
        temp_supplier.mobile_phone,
        temp_supplier.fax_number,
        temp_supplier.address,
        temp_supplier.city,
        temp_supplier.state_province,
        temp_supplier.zip_postal_code,
        temp_supplier.country_region,
        temp_supplier.web_page,
        temp_supplier.notes
    )   
    cursor.execute(statement, list(values)+[updateId])
    
    return redirect("suppliers")
    
def delete_record(cursor,updateId):
    statement ="DELETE FROM suppliers WHERE ID=%s;"   
    cursor.execute(statement, (updateId,))

    #statement="INSERT INTO TableLastUpdateInfo VALUES('Suppliers',CURRENT_TIMESTAMP());"
    #cursor.execute(statement)
        
def index(db,current_user):
    cursor = db.cursor()
    if request.method =='POST':
        operation=request.form["operation"]
        if operation == "0":#add new record
            temp_supplier=Supplier()
    
            #new record
            temp_supplier.company=request.form["company"]
            temp_supplier.last_name=request.form["last_name"]
            temp_supplier.first_name=request.form["first_name"]
            temp_supplier.email_address=request.form["email_address"]
            temp_supplier.job_title=request.form["job_title"]
            temp_supplier.home_phone=request.form["home_phone"]
            temp_supplier.business_phone=request.form["business_phone"]
            temp_supplier.mobile_phone=request.form["mobile_phone"]
            temp_supplier.fax_number=request.form["fax_number"]
            temp_supplier.address=request.form["address"]
            temp_supplier.city=request.form["city"]
            temp_supplier.state_province=request.form["state_province"]
            temp_supplier.zip_postal_code=request.form["zip_postal_code"]
            temp_supplier.country_region=request.form["country_region"]
            temp_supplier.web_page=request.form["web_page"]
            temp_supplier.notes=request.form["notes"]
            
            create_record(cursor,temp_supplier)
        
        elif operation=="1":#delete
            updateId= request.form["updateId"]
            delete_record(cursor,updateId)
        elif operation=="2":#update
            temp_supplier=Supplier()
            #updated record
            temp_supplier.company=request.form["company"]
            temp_supplier.last_name=request.form["last_name"]
            temp_supplier.first_name=request.form["first_name"]
            temp_supplier.email_address=request.form["email_address"]
            temp_supplier.job_title=request.form["job_title"]
            temp_supplier.home_phone=request.form["home_phone"]
            temp_supplier.business_phone=request.form["business_phone"]
            temp_supplier.mobile_phone=request.form["mobile_phone"]
            temp_supplier.fax_number=request.form["fax_number"]
            temp_supplier.address=request.form["address"]
            temp_supplier.city=request.form["city"]
            temp_supplier.state_province=request.form["state_province"]
            temp_supplier.zip_postal_code=request.form["zip_postal_code"]
            temp_supplier.country_region=request.form["country_region"]
            temp_supplier.web_page=request.form["web_page"]
            temp_supplier.notes=request.form["notes"]
            updateId= request.form["updateId"]            
            update_record(cursor,updateId,temp_supplier)
        now = datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE TableLastUpdateInfo SET update_time=%s WHERE table_name='suppliers';",(formatted_time,))    
        db.commit()#commit for all operations        
        
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()
   
    cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='suppliers';")
    update_time=cursor.fetchall()
    update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone

    cursor.close()
    return render_template('suppliers.html', records=records,update_time=update_time,status=current_user.status)

def get_supplier_company(db):
    cursor = db.cursor()
    supplier_list = []
    select_query = """ SELECT DISTINCT id, company FROM suppliers ORDER BY id """
    cursor.execute(select_query)
    for company, id in cursor:
        supplier_list.append((company, id))
    cursor.close()
    return supplier_list

