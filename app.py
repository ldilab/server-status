import os
import time
from os.path import join, dirname

import flask
import requests
from dotenv import load_dotenv
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

from src.inspector import Monitor
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()
auth = HTTPBasicAuth()
inspector = Monitor(update_interval=30)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

users = {
    os.environ.get("username"): generate_password_hash(os.environ.get("password"))
}

if os.environ.get("nodes") is not None:
    subs = {
        node: port
        for node, port in zip(os.environ.get("nodes").split(","), os.environ.get("ports").split(","))
    }
else:
    subs = {}


@scheduler.task('interval', id='self_update', seconds=inspector.update_interval)
def my_job():
    inspector.update()


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/")
@auth.login_required
def my_status():
    return flask.jsonify(
        inspector.get_all_info()
    )


@app.route("/<node>")
@auth.login_required
def node_status(node):
    if node not in subs:
        return flask.jsonify(
            {
                "error": "Node not found"
            }
        )

    current_time = time.time()
    if current_time - inspector.last_update > inspector.update_interval:
        inspector.update()

    return requests.get(f"http://{node}:{subs[node]}/", auth=tuple(auth.get_auth().parameters.values())).json()


scheduler.init_app(app)
scheduler.start()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    app.run(debug=True, host='0.0.0.0', port=port)
