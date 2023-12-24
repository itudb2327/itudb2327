import mysql.connector
from flask import Flask, render_template, request,redirect,session
import time
from datetime import datetime, timedelta
import math
from geopy.geocoders import Nominatim

# Define the 'Supplier' class to represent supplier objects
class Supplier:
    def __init__(self, id=None, company=None, last_name=None, first_name=None, email_address=None,
                        job_title=None,business_phone=None, address=None,zip_postal_code=None, notes=None):
        self.id = id
        self.company = company
        self.last_name = last_name
        self.first_name = first_name
        self.email_address = email_address
        self.job_title = job_title
        self.business_phone = business_phone
        self.address = address
        self.zip_postal_code = zip_postal_code
        self.notes = notes
            
        
# Function to convert a list of records to a list of 'Supplier' objects
def list_to_object(records):
    supplier_list=[]
    for record in records:
        supplier = Supplier(
            id=record[0],
            company=record[1],
            last_name=record[2],
            first_name=record[3],
            email_address=record[4],
            job_title=record[5],
            business_phone=record[6],
            address=record[7],
            zip_postal_code=record[8],
            notes=record[9]
        )
        supplier_list.append(supplier)
    return supplier_list
# Function to create a new supplier record in the database
def create_record(cursor,temp_supplier):
    

    statement = """
        INSERT INTO suppliers (
            company,
            last_name,
            first_name,
            email_address,
            job_title,
            business_phone,
            address,
            zip_postal_code,
            notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
      """

    
    values = (
        temp_supplier.company,
        temp_supplier.last_name,
        temp_supplier.first_name,
        temp_supplier.email_address,
        temp_supplier.job_title,
        temp_supplier.business_phone,
        temp_supplier.address,
        temp_supplier.zip_postal_code,
        temp_supplier.notes
    )   
    cursor.execute(statement, values)

    return redirect("suppliers")
# Function to update an existing supplier record in the database
def update_record(cursor,updateId,temp_supplier):
    print(updateId)
    statement = """
        UPDATE suppliers SET
            company=%s,
            last_name=%s,
            first_name=%s,
            email_address=%s,
            job_title=%s,
            business_phone=%s,
            address=%s,
            zip_postal_code=%s,
            notes=%s

        WHERE ID=%s;
      """

    
    values = (
        temp_supplier.company,
        temp_supplier.last_name,
        temp_supplier.first_name,
        temp_supplier.email_address,
        temp_supplier.job_title,
        temp_supplier.business_phone,
        temp_supplier.address,
        temp_supplier.zip_postal_code,
        temp_supplier.notes
    )   
    cursor.execute(statement, list(values)+[updateId])
    
    return redirect("suppliers")
# Function to delete a supplier record from the database    
def delete_record(cursor,updateId):
    statement ="DELETE FROM suppliers WHERE ID=%s;"   
    cursor.execute(statement, (updateId,))

    #statement="INSERT INTO TableLastUpdateInfo VALUES('Suppliers',CURRENT_TIMESTAMP());"
    #cursor.execute(statement)

# Main function to handle requests and render the suppliers page        
def index(db,current_user):
    cursor = db.cursor()
    nearest_supplier=None
    most_profit=None
    print(request.form.keys())
    if request.method =='POST':
        if 'operation' in request.form:
            operation=request.form["operation"]
            print(operation)
            if operation == "0":#add new record
                temp_supplier=Supplier()
                
                #new record
                temp_supplier.company=request.form["company"] if request.form["company"] else None
                temp_supplier.last_name=request.form["last_name"] if request.form["last_name"] else None
                temp_supplier.first_name=request.form["first_name"] if request.form["first_name"] else None
                temp_supplier.email_address=request.form["email_address"] if request.form["email_address"] else None
                temp_supplier.job_title=request.form["job_title"] if request.form["job_title"] else None
                temp_supplier.business_phone=request.form["business_phone"] if request.form["business_phone"] else None
                temp_supplier.address=request.form["address"] if request.form["address"] else None
                temp_supplier.zip_postal_code=request.form["zip_postal_code"] if request.form["zip_postal_code"] else None
                temp_supplier.notes=request.form["notes"] if request.form["notes"] else None
                
                create_record(cursor,temp_supplier)
            
            elif operation=="1":#delete
                updateId= request.form["updateIdHidden_conf"]
                delete_record(cursor,updateId)
            elif operation=="2":#update
                temp_supplier=Supplier()
                
                #updated record
                temp_supplier.company=request.form["u_company"]
                temp_supplier.last_name=request.form["u_last_name"]
                temp_supplier.first_name=request.form["u_first_name"]
                temp_supplier.email_address=request.form["u_email_address"]
                temp_supplier.job_title=request.form["u_job_title"]
                temp_supplier.business_phone=request.form["u_business_phone"]
                temp_supplier.address=request.form["u_address"]
                temp_supplier.zip_postal_code=request.form["u_zip_postal_code"]
                temp_supplier.notes=request.form["u_notes"]
                updateId= request.form["updateIdHidden"]          
                update_record(cursor,updateId,temp_supplier)
            now = datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
             # Update the last update time in the database
            cursor.execute("UPDATE TableLastUpdateInfo SET update_time=%s WHERE table_name='suppliers';",(formatted_time,))    
            db.commit()#commit for all operations        
        # Check for latitude and longitude submission  
        elif 'latitude' in request.form:
            lat=request.form["latitude"]
            long=request.form["longitude"]
            target_coord=(float(lat),float(long))
            nearest_supplier=find_nearest_supplier(db,target_coord)[0][0]
         # Check for profit calculation submission    
        elif 'profit_call' in request.form: 
            most_profit=profit(cursor)
            
    cursor.execute("SELECT * FROM suppliers;")
    records = cursor.fetchall()
    records=list_to_object(records)
    print(most_profit)
   
   
    update_time=display_last_update(cursor)
        
    return render_template('suppliers.html', records=records,update_time=update_time,status=current_user.status,nearest_supplier=nearest_supplier,current_supplier=None,most_profit=most_profit)
# Function to calculate the most profitable suppliers
def profit(cursor):

    cursor.execute("""
       WITH SupplierPaymentAverage AS (
    SELECT
        P.supplier_id,
        AVG(P.payment_amount) AS AvgPaymentAmount,
		MAX(P.payment_amount)     AS MaxAmount
    FROM
        purchase_orders P
    WHERE
        P.status_id = '2'
    GROUP BY
        P.supplier_id
),
OverallPaymentAverage AS (
    SELECT
        AVG(P.payment_amount) AS OverallAvgPayment
    FROM
        purchase_orders P
    WHERE
        P.status_id = '2'
)

SELECT
    S.company,
    P.AvgPaymentAmount,
    ((P.AvgPaymentAmount-O.OverallAvgPayment)/O.OverallAvgPayment)*100 as sd,
    P.MaxAmount
    
FROM
    suppliers S
JOIN
    SupplierPaymentAverage P ON S.id = P.supplier_id
JOIN
    OverallPaymentAverage O ON 1=1
WHERE
    P.AvgPaymentAmount > O.OverallAvgPayment
ORDER BY
    P.AvgPaymentAmount DESC;


    """)

    profit=cursor.fetchall()
    return profit
# Function to retrieve a list of supplier companies from the database
def get_supplier_company(db):
    cursor = db.cursor()
    supplier_list = []
    select_query = """ SELECT DISTINCT id, company FROM suppliers ORDER BY id """
    cursor.execute(select_query)
    for company, id in cursor:
        supplier_list.append((company, id))
    cursor.close()
    return supplier_list



# Function to calculate the Haversine distance between two sets of latitude and longitude coordinates
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

    
# Function to find the nearest supplier based on target coordinates
def find_nearest_supplier(db,target_coords):
    zipcodes_with_coords = {}
    select_query="SELECT zip_postal_code from suppliers;"
    cursor = db.cursor()
    cursor.execute(select_query)
    zipcodes=cursor.fetchall()
    cursor.close()
    # Retrieve coordinates for each zip code
    for zipcode in zipcodes:
        coords = get_lat_lon(zipcode)
        if coords:
            zipcodes_with_coords[zipcode] = coords
     
    min_distance = float('inf')
    nearest_zipcode = None
    # Calculate distance for each zip code and find the nearest one
    for zipcode, coords in zipcodes_with_coords.items():
        distance = haversine(target_coords[0], target_coords[1], coords[0], coords[1])
        if distance < min_distance:
            min_distance = distance
            nearest_zipcode = zipcode
    
    select_query="SELECT company from suppliers WHERE zip_postal_code=%s;"
    cursor = db.cursor()
     # Retrieve the company name of the nearest supplier
    cursor.execute(select_query,nearest_zipcode)
    nearest_supplier=cursor.fetchall()
    cursor.close()
    return nearest_supplier  
    
    

# Function to retrieve latitude and longitude coordinates for a given zip code using geocoding
def get_lat_lon(zipcode):
    geolocator = Nominatim(user_agent="suppliers")
    location = geolocator.geocode(zipcode)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Function to display the last update time for the purchase orders table
def display_last_update(cursor):
        cursor.execute("SELECT update_time FROM TableLastUpdateInfo where table_name='purchase_orders';")
        update_time=cursor.fetchall()
        update_time=(update_time[0][0]).strftime("%Y-%m-%d %H:%M:%S")#reaching timestamp information and adjust it to UTC+03:00 timezone
        cursor.close()
        return update_time