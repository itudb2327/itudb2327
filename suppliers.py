import mysql.connector
from flask import Flask, render_template, request,redirect
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
        
    def print_info(self):
        print(f"ID: {self.id}")
        print(f"Company: {self.company}")
        print(f"Last Name: {self.last_name}")
        print(f"First Name: {self.first_name}")
        print(f"Email Address: {self.email_address}")
        print(f"Job Title: {self.job_title}")
        print(f"Business Phone: {self.business_phone}")
        print(f"Home Phone: {self.home_phone}")
        print(f"Mobile Phone: {self.mobile_phone}")
        print(f"Fax Number: {self.fax_number}")
        print(f"Address: {self.address}")
        print(f"City: {self.city}")
        print(f"State/Province: {self.state_province}")
        print(f"ZIP/Postal Code: {self.zip_postal_code}")
        print(f"Country/Region: {self.country_region}")
        print(f"Web Page: {self.web_page}")
        print(f"Notes: {self.notes}")
        print(f"Attachments: {self.attachments}")        
        
        
def index(db):
    if request.method =='POST':
    
        operation=request.form["operation"]
        
        if operation == "0":#add new record
        
            temp_supplier=Supplier()
            
            #new record
            temp_supplier.company=request.form.get("company")
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
            cursor = db.cursor()    
            cursor.execute(statement, values)
            db.commit()
            cursor.close()

            return redirect("suppliers")
        elif operation=="1":#delete
            updateId= request.form["updateId"]
            statement ="DELETE FROM suppliers WHERE ID=%s;"
            cursor = db.cursor()    
            cursor.execute(statement, (updateId,))
            db.commit()
            cursor.close()
        elif operation=="2":#update
            #update record
            pass
            print(request.form)
          
            print(request.form["updateId"])
            
        
        
    cursor = db.cursor()
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()
    cursor.close()
    

    return render_template('suppliers.html', records=records)
