from flask import Flask, redirect, url_for
import secrets
from initialization import init
from blueprints.employee_blueprint import employee_services
from blueprints.user_blueprint import user_services

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.register_blueprint(user_services, url_prefix="/users")
app.register_blueprint(employee_services, url_prefix="/employees")
init()


@app.route('/')
def home():
    return redirect(url_for('user_services.login'))


if __name__ == '__main__':
    app.run(debug=True)
