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
        employees = DB.select_query('SELECT * FROM employee ORDER BY employee.date_started ASC')
        return render_template("dashboard.html", employees=employees)

    if request.method == 'POST':
        pass
