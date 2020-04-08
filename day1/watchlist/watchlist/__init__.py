import os, sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"   # win平台
else:
    prefix = "sqlite:////"    # 非win平台

app = Flask(__name__)


# 设置数据库的URI
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
# 优化内存
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'env')


# 初始化
db = SQLAlchemy(app)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接收用户ID作为参数
    from watchlist.models import User
    user = User.query.get(user_id)
    return user

# 如果没有登陆有些操作不被允许
login_manager.login_view = 'login'


# 模板上下文处理函数
@app.context_processor
def common_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)



from watchlist import views, models, errors, commands

