import os
import time
from os.path import join, dirname

import flask
from dotenv import load_dotenv
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

from src.inspector import Monitor

app = Flask(__name__)
auth = HTTPBasicAuth()
inspector = Monitor(update_interval=10)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

users = {
    os.environ.get("username"): generate_password_hash(os.environ.get("password"))
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/")
@auth.login_required
def hello_world():
    current_time = time.time()
    if current_time - inspector.last_update > inspector.update_interval:
        inspector.update()

    return flask.jsonify(
        inspector.get_all_info()
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
