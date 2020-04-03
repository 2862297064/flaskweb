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

    movies = Movie.query.all()

    return render_template("index.html", movies=movies)


# 自定义命令
# 建立空数据库
@app.cli.command()   # 注册为命令
@click.option("--drop", is_flag=True, help="先删除再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")


# 向空数据库中插入数据
@app.cli.command()
def forge():
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
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m["title"], year=m["year"])
        db.session.add(movie)
    db.session.commit()
    click.echo("数据添加完成")


# 错误函数处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)





