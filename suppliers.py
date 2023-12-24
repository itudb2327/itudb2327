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
    nearest_supplier=None
    if request.method =='POST':
        if 'operation' in request.form:
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
        elif 'latitude' in request.form:
            lat=request.form["latitude"]
            long=request.form["longitude"]
            target_coord=(float(lat),float(long))
            nearest_supplier=find_nearest_supplier(db,target_coord)[0][0]
            
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()
   
    update_time=display_last_update(cursor)

    return render_template('suppliers.html', records=records,update_time=update_time,status=current_user.status,nearest_supplier=nearest_supplier)

def get_supplier_company(db):
    cursor = db.cursor()
    supplier_list = []
    select_query = """ SELECT DISTINCT id, company FROM suppliers ORDER BY id """
    cursor.execute(select_query)
    for company, id in cursor:
        supplier_list.append((company, id))
    cursor.close()
    return supplier_list

import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in miles
    R = 3958.8

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

    
    
def find_nearest_supplier(db,target_coords):
    zipcodes_with_coords = {}
    select_query="SELECT zip_postal_code from suppliers;"
    cursor = db.cursor()
    cursor.execute(select_query)
    zipcodes=cursor.fetchall()
    cursor.close()
    
    for zipcode in zipcodes:
        coords = get_lat_lon(zipcode)
        if coords:
            zipcodes_with_coords[zipcode] = coords
     
    min_distance = float('inf')
    nearest_zipcode = None

    for zipcode, coords in zipcodes_with_coords.items():
        distance = haversine(target_coords[0], target_coords[1], coords[0], coords[1])
        if distance < min_distance:
            min_distance = distance
            nearest_zipcode = zipcode
    
    select_query="SELECT company from suppliers WHERE zip_postal_code=%s;"
    cursor = db.cursor()
    
    cursor.execute(select_query,nearest_zipcode)
    nearest_supplier=cursor.fetchall()
    cursor.close()
    return nearest_supplier  
    
    
from geopy.geocoders import Nominatim

def get_lat_lon(zipcode):
    geolocator = Nominatim(user_agent="suppliers")
    location = geolocator.geocode(zipcode)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None


def display_last_update(cursor):
        cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='purchase_orders';")
        update_time=cursor.fetchall()
        update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone
        cursor.close()
        return update_time