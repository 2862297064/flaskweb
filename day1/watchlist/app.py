import os, sys


from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import click


WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"   # win平台
else:
    prefix = "sqlite:////"    # 非win平台

app = Flask(__name__)

# 设置数据库的URI
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, 'data.db')

# 优化内存
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化
db = SQLAlchemy(app)


# -------------------------models   数据层

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# views ----------------------------视图函数

@app.route("/")
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


# 自定义命令
@app.cli.command()   # 注册为命令
@click.option("--drop", is_flag=True, help="先删除再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")

