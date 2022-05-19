from database.DB import DB
from models.user import User
from flask import Blueprint, request, session, redirect, url_for, render_template


user_services = Blueprint("user_services", __name__)
db = DB.connect()


@user_services.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'Authorization' in session:
            return redirect(url_for('employee_services.dashboard'))
        else:
            msg = ''
            return render_template('login.html', msg=msg)

    if request.method == 'POST':
        msg = ''
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            is_username = DB.select_query(
                'SELECT COUNT(username) FROM user WHERE username = %s', (username,))
            is_username = is_username[0]['COUNT(username)']

            if is_username == 1:
                stored_password = DB.select_query(
                    'SELECT password FROM user WHERE username = %s', (username,))
                stored_password = stored_password[0]['password']

                if User.verify_password(stored_password, password):
                    session['Authorization'] = True
                    session['username'] = username
                    return redirect(url_for('employee_services.dashboard'))
                else:
                    msg = 'Username and/or password is not correct!'
                    return render_template('login.html', msg=msg)
            else:
                msg = 'Username and/or password is not correct!'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Check your details, and try to login again!'
            return render_template('login.html', msg=msg)

