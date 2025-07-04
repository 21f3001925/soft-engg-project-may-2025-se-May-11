from flask import Flask
from scheduler import start_scheduler

app = Flask(__name__)

start_scheduler()


@app.route("/")
def hello_world():
    return "Hello, World! from Backend"


if __name__ == "__main__":
    app.run(debug=True)
