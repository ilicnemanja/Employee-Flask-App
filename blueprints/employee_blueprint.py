import re
from database.DB import DB
from models.employee import Employee
from flask import Blueprint, request, session, redirect, url_for, render_template, abort
from functools import wraps


employee_services = Blueprint("employee_services", __name__)

db = DB.connect()

# FOR REGISTER
# DB.insert_into_query("INSERT INTO employee VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s)",
#                      (employee.first_name, employee.last_name, employee.email, employee.role,
#                       employee.linked_in, employee.salary, employee.photo, employee.date_started))


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' in session:
            return f(*args, **kws)
        else:
            abort(401)
    return decorated_function


@employee_services.route('/', methods=['GET', 'POST'])
@authorize
def dashboard():
    if request.method == 'GET':
        employees = DB.select_query(
            'SELECT * FROM employee ORDER BY employee.date_started ASC')
        return render_template("dashboard.html", employees=employees)

    if request.method == 'POST':
        pass


@employee_services.route('/profile/<id>', methods=['GET', 'POST'])
@authorize
def employee_profile(id):
    if request.method == 'GET':
        employee = DB.select_query('SELECT * FROM employee WHERE id=%s', (id,))
        employee = employee[0]
        return render_template('employee/employee_profile.html', employee=employee)
    if request.method == 'POST':
        pass


@employee_services.route('/delete/<id>', methods=['GET'])
@authorize
def delete(id):

    # employee = DB.select_query('SELECT * FROM employee WHERE id=%s', (id,))
    # photoUrl = employee[0]['photo_url']
    # if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl)) and photoUrl != "":
    #     os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).rindex(os.path.sep)], "static" + photoUrl))

    DB.delete_query(table_name='employee', condition='id', data=id)
    return redirect(url_for('employee_services.dashboard'))
