import os
import time

from flask import Flask

from src.inspector import Monitor

app = Flask(__name__)
inspector = Monitor(update_interval=10)


@app.route("/")
def hello_world():
    current_time = time.time()
    if current_time - inspector.last_update > inspector.update_interval:
        inspector.update()

    return inspector.get_all_info()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
