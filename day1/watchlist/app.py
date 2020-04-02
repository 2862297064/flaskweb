from flask import Flask, url_for, render_template

app = Flask(__name__)


# @app.route("/")
# @app.route("/index/")
# @app.route("/home/")
# def index():
#     return "hello word david111!"


@app.route("/user/")
def index():
    name = "David"
    movies = [
        {"title": "大赢家", "year": "2020"},
        {"title": "囧妈", "year": "2020"},
        {"title": "叶问", "year": "2020"},
        {"title": "疯狂外星人", "year": "2019"},
        {"title": "大话西游", "year": "1999"},
        {"title": "月光宝盒", "year": "1996"},
        {"title": "速度与激情8", "year": "2020"}
    ]
    return render_template("index.html", name=name, movies=movies)


