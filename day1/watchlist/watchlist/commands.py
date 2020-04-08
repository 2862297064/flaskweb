import click
from watchlist import db, app
from watchlist.models import Movie, UserMixin

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