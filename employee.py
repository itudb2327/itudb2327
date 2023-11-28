import mysql.connector

class Employees:
    def __init__(self, name, surname, job_title, phone_number, note) :
        self.name= name
        self.surname =surname
        self.job_title = job_title
        self.phone_number = phone_number
        self.note = note

    def get_all_employees(db):
        cursor = db.cursor()
        employee_list = []
        select_query=""" SELECT id, first_name, last_name, job_title, business_phone, notes FROM employees """
        cursor.execute(select_query)
        for employee_id, first_name, last_name, job_title, business_phone, notes in cursor:
            employee_list.append((employee_id, Employees(first_name,last_name, job_title, business_phone, notes)))
        cursor.close()
        return employee_list
    def search_employee(name, employee_list):
        filtered_employee = []
        for employee_id, employee in employee_list:
            full_name = employee.name + ' ' + employee.surname
            if name in full_name.upper(): 
                filtered_employee.append((employee_id, employee))
        return filtered_employee
    def add_employee(db, new_employee):
        cursor= db.cursor()
        query= """ INSERT INTO employees (last_name, first_name, job_title, business_phone, notes)
          VALUES (%s, %s, %s, %s, %s) """
        values= (new_employee.surname, new_employee.name, new_employee.job_title, new_employee.phone_number, new_employee.note)
        cursor.execute(query, values)
        
