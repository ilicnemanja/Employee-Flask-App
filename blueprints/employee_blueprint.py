from database.DB import DB
from models.employee import Employee
from flask import Blueprint, request, session, redirect, url_for, render_template, abort, flash
from functools import wraps
from upload import upload_file
import os


employee_services = Blueprint("employee_services", __name__)
db = DB.connect()


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' in session:
            return f(*args, **kws)
        else:
            abort(401)
    return decorated_function


def replace_sep(employees: list):
    if isinstance(employees, str):
        employees = employees.replace('\\', '/')
        return employees
    elif employees == None:
        return ''
    elif len(employees) == 1:
        employee = employees[0]
        if employee['photo'] != None and employee['photo'] != '':
            employee['photo'] = employee['photo'].replace('\\', '/')
    else:
        for employee in employees:
            if employee['photo'] != None:
                employee['photo'] = employee['photo'].replace('\\', '/')


@ employee_services.route('/', methods=['GET', 'POST'])
@ authorize
def dashboard():
    if request.method == 'GET':
        employees = DB.select_query(
            'SELECT * FROM employee ORDER BY employee.date_started DESC')

        replace_sep(employees)

        return render_template("dashboard.html", employees=employees)
    if request.method == 'POST':
        pass


@ employee_services.route('/add-employee', methods=['GET', 'POST'])
@ authorize
def add_employee():
    if request.method == 'GET':
        return render_template('employee/add_employee.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role']
        salary = request.form['salary']
        email = request.form['email']
        linked_in = request.form['linked_in']
        photoUrl = request.files['photoUrl']

        employee = Employee(None, first_name, last_name, email,
                            role, linked_in, salary, photoUrl)

        cursor = db.cursor(prepared=True)
        cursor.execute(
            "SELECT * FROM employee  WHERE email=%s", (employee.email,))
        is_email = cursor.fetchone()

        cursor = db.cursor(prepared=True)
        cursor.execute(
            "SELECT * FROM employee  WHERE linked_in=%s", (employee.linked_in,))
        is_linkedin = cursor.fetchone()

        if is_email != None:
            photoUrl = False
            return render_template("employee/add_employee.html", msg="This email is already registered", employee=employee)
        if is_linkedin != None:
            photoUrl = False
            return render_template("employee/add_employee.html", msg="This linkedIn is already registered", employee=employee)

        photoUrl = upload_file()
        if photoUrl == False:
            return render_template("employee/add_employee.html", msg="Invalid type of file", employee=employee)

        DB.insert_into_query("INSERT INTO employee VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (employee.first_name, employee.last_name, employee.email, employee.role,
                                 employee.linked_in, employee.salary, photoUrl, employee.date_started))
        flash('Employee Added Successfully')
        return redirect(url_for("employee_services.dashboard"))


@ employee_services.route('/profile-employee/<id>', methods=['GET', 'POST'])
@ authorize
def employee_profile(id):
    if request.method == 'GET':
        employee = DB.select_query('SELECT * FROM employee WHERE id=%s', (id,))

        replace_sep(employee)

        employee = employee[0]
        return render_template('employee/employee_profile.html', employee=employee)
    if request.method == 'POST':
        cursor = db.cursor(prepared=True)
        cursor.execute("SELECT * FROM employee WHERE id=%s", (id,))
        row = cursor.fetchone()
        photo_in_db = row[7]
        photo_in_db_modif = replace_sep(row[7])

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role']
        salary = request.form['salary']
        email = request.form['email']
        linked_in = request.form['linked_in']
        photoUrl = request.files['photoUrl']
        delete_photo = request.form['deletePhoto']
        photoUrl = upload_file()

        DB.update_query(
            f"""UPDATE employee SET first_name=%s, last_name=%s, role=%s, email=%s, linked_in=%s, salary=%s, photo=%s WHERE `id`={id}""", (first_name, last_name, role, email, linked_in, salary, photoUrl))

        if delete_photo == '1' and photo_in_db != "":
            if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photo_in_db_modif)):
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__))[
                    :os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photo_in_db_modif))
            photoUrl = ''
        elif delete_photo == '1' and photoUrl != "":
            if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl)):
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(
                    os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl))
            photoUrl = ''
        elif photoUrl == '' and photo_in_db != '':
            photoUrl = photo_in_db
        elif photoUrl != photo_in_db:
            if photo_in_db != '':
                if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photo_in_db_modif)):
                    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__))[
                        :os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photo_in_db_modif))
        return redirect(url_for("employee_services.employee_profile", id=id))


@ employee_services.route('/delete/<id>', methods=['GET'])
@ authorize
def delete(id):
    q = "SELECT * FROM employee WHERE id=%s"
    parameters = (id,)
    employee = DB.select_query(query_string=q, parameters=parameters)
    photoUrl = employee[0]['photo']
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl)) and photoUrl != "":
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(
            os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl))
    table = "employee"
    condition = "id"
    data = id
    DB.delete_query(table_name=table, condition=condition, data=data)
    flash('Employee Removed Successfully')
    return redirect(url_for('employee_services.dashboard'))
