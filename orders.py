import mysql.connector
from flask import Flask, render_template, request,redirect,session
def index(db):
    
    cursor = db.cursor()
    active_filter="-1"
    records=[]
    if request.method =='POST':
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
        # db.commit()#commit for all filters        

   

    return render_template('orders.html',records=records,active_filter=active_filter)