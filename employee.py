import mysql.connector
from flask import Flask, render_template, request, flash
class Employees:
    def __init__(self, name, surname, job_title, phone_number, note) :
        self.name= name
        self.surname =surname
        self.job_title = job_title
        self.phone_number = phone_number
        self.note = note

    def index(db):
        jobs = Employees. get_all_jobtitle(db)
        employee_list= Employees.get_all_employees(db)
        if request.method == "POST":
            if("first_name" in request.form):
                return Employees.add_employee(db)
            elif("search" in request.form):
                return Employees.search_employee(db)      
            elif("deleteId" in request.form):
                return Employees.delete_employee(db)            
            elif("updateId" in request.form):
                return Employees.update_employee(db)   
            elif ("choosenJob" in request.form): 
                return Employees.get_filtered_job(db)
            else:
                return render_template("employees.html", employee_list=employee_list, jobs=jobs)
        else:
            return render_template("employees.html", employee_list=employee_list, jobs=jobs)
    
    def get_all_employees(db):
        job_list = Employees.get_all_jobtitle(db)
        cursor = db.cursor()
        employee_list = []
        select_query=""" SELECT id, first_name, last_name, job_title, business_phone, notes FROM employees """
        cursor.execute(select_query)
        for employee_id, first_name, last_name, job_title, business_phone, notes in cursor:
            employee_list.append((employee_id, Employees(first_name,last_name, job_title, business_phone, notes)))
        cursor.close()
        return employee_list
    def search_employee(db):
        employee_list = Employees.get_all_employees(db)
        job_list = Employees.get_all_jobtitle(db)
        employee_name =request.form['search']
        employee_name = employee_name.upper()
        filtered_employee = []
        for employee_id, employee in employee_list:
            full_name = employee.name + ' ' + employee.surname
            if employee_name in full_name.upper(): 
                filtered_employee.append((employee_id, employee))
        return render_template("employees.html", employee_list=filtered_employee, jobs =job_list)
        
    def add_employee(db):
        job_list = Employees.get_all_jobtitle(db)
        new_employee = Employees(request.form['first_name'], 
                                 request.form['last_name'],
                                 request.form['job_title'],
                                 request.form['phone_number'],
                                 request.form['extra_notes'])
        cursor= db.cursor()
        query= """ INSERT INTO employees (last_name, first_name, job_title, business_phone, notes)
          VALUES (%s, %s, %s, %s, %s) """
        
        values= (new_employee.surname, new_employee.name, new_employee.job_title, new_employee.phone_number, new_employee.note)
        cursor.execute(query, values)
        db.commit()
        new_list = Employees.get_all_employees(db)
        return render_template("employees.html", employee_list=new_list, jobs =job_list)
        
    def delete_employee(db):
        deletedEmployeeId = request.form['deleteId']
        cursor = db.cursor()
        job_list = Employees.get_all_jobtitle(db)
        delete_query = f"DELETE FROM employees WHERE id = '{deletedEmployeeId}'"
        cursor.execute(delete_query)
        db.commit()
        new_list = Employees.get_all_employees(db)
        return render_template("employees.html", employee_list=new_list, jobs =job_list)
    def update_employee( db):
        job_list = Employees.get_all_jobtitle(db)
        updatedEmployeeId = request.form['updateId']
        new_employee = Employees(request.form['newFirst_name'], 
                                 request.form['newLast_name'],
                                 request.form['newJob_title'],
                                 request.form['newPhone_number'],
                                 request.form['newExtra_notes'])
        cursor= db.cursor()
        query= """ UPDATE employees SET last_name = %s, first_name=%s, job_title=%s, business_phone=%s, notes=%s
         WHERE ID = %s """
        values= (new_employee.surname, new_employee.name, new_employee.job_title, new_employee.phone_number, new_employee.note, updatedEmployeeId)
        cursor.execute(query, values)
        db.commit()
        new_list = Employees.get_all_employees(db)
        return render_template("employees.html", employee_list=new_list, jobs =job_list)
    
    def get_all_jobtitle(db):
        jobtitle_list = []
        cursor = db.cursor()
        select_query = """ SELECT DISTINCT job_title FROM employees """
        cursor.execute(select_query)
        for job in cursor:
            jobtitle_list.append(job)
        cursor.close()
        return jobtitle_list
    def get_filtered_job(db):
        selected_job = request.form.get('choosenJob')
        job_list = Employees.get_all_jobtitle(db)
        if(selected_job=='all'):
            employee_list = Employees.get_all_employees(db)
            return render_template("employees.html", employee_list=employee_list, jobs =job_list)
        filtered_employees = []
        values = []
        values.append(selected_job)
        cursor = db.cursor()
        query= """
                SELECT id, first_name, last_name, job_title, business_phone, notes FROM employees WHERE job_title=%s;
                """
        
        cursor.execute(query, values)
        
        for employee_id, first_name, last_name, job_title, business_phone, notes in cursor:
            filtered_employees.append((employee_id, Employees(first_name,last_name, job_title, business_phone, notes)))
        cursor.close()

        
        return render_template("employees.html", employee_list=filtered_employees, jobs =job_list)
    