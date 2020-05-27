import os, sys
from flask_sqlalchemy import SQLAlchemy #数据库类导入
from flask import Flask
from flask_login import LoginManager
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY']='nihao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2468QAZwsx@@43.255.231.253:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控

db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from myapp.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

login_manager.login_view = 'login'

# @app.context_processor
# def inject_user():
#     from myapp.models import User
#     user = User.query.first()
#     return dict(user=user)

from myapp.views import app
from myapp.errors import app






if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)