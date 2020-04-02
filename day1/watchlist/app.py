from flask import Flask

app = Flask(__name__)


# @app.route("/")
# @app.route("/index/")
# @app.route("/home/")
# def index():
#     return "hello word david111!"


@app.route("/user/<name>")
def index(name):
    return "hello %s"%name


