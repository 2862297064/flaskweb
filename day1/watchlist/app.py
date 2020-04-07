import os, sys


from flask import Flask, url_for, render_template, request, flash, redirect

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

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

app.config["SECRET_KEY"] = '1903_dev'

# 初始化
db = SQLAlchemy(app)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接收用户ID作为参数
    user = User.query.get(user_id)
    return user

# 如果没有登陆有些操作不被允许
login_manager.login_view = 'login'


# -------------------------models   数据层
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) 
    username = db.Column(db.String(20)) 
    password_hash = db.Column(db.String(128)) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# views ----------------------------视图函数

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        # 获取表单数据
        title = request.form.get("title")
        year = request.form.get("year")
        # 验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash("输入错误")
            return redirect(url_for("index"))
        # 将数据保存到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("创建成功")
        return redirect(url_for("index"))

    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


# 更新/movie/edit
@app.route('/movie/edit/<int:movie_id>', methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        if not title or not year or len(year)>4 or len(title)>60:
            flash("输入有误")
            return redirect(url_for("edit"), movie_id=movie_id)
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("电影更新完成")
        return redirect(url_for("index"))
    return render_template("edit.html", movie=movie)


# delete
@app.route("/movie/delete/<int:movie_id>", methods=["POST", "GET"])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for("index"))


# 登录
@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            flash("输入有误")
            return redirect(url_for("login"))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("登陆成功")
            return redirect(url_for('index'))
        flash('验证失败')
        return redirect(url_for('login'))
    return render_template('login.html')


# logout
@app.route('/logout/')
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('index'))


# settings设置
@app.route('/settings/', methods=["POST", "GET"])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash("输入错误")
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash("名字已更新")
        return redirect(url_for('index'))
    return render_template('settings.html')

 
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
    # name = "David"
    movies = [
        {"title": "大赢家", "year": "2020"},
        {"title": "囧妈", "year": "2020"},
        {"title": "叶问", "year": "2020"},
        {"title": "疯狂外星人", "year": "2019"},
        {"title": "大话西游", "year": "1999"},
        {"title": "月光宝盒", "year": "1996"},
        {"title": "速度与激情8", "year": "2020"}
    ]
    # user = User(name=name)
    # db.session.add(user)
    for m in movies:
        movie = Movie(title=m["title"], year=m["year"])
        db.session.add(movie)
    db.session.commit()
    click.echo("数据添加完成")


# 自定义指令，生成管理员账户
# 输入用户名admin，密码，确认密码
@app.cli.command()
@click.option("--username", prompt=True, help="登陆的用户名")
@click.option("--password", prompt=True, help="登陆的密码",  confirmation_prompt=True, hide_input=True)
def admin(username, password):
    user = User.query.first()
    if user is not None:
        click.echo("更新管理员账户")
        user.username = username
        user.set_password(password)
    else:
        click.echo("创建管理员账户")
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("管理员账户更新/创建完成")


# 错误函数处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)





