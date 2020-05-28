from flask_login import login_user,logout_user,login_required,UserMixin
from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model,UserMixin):  # 表名将会是 user（自动生成，小写处理）
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20),unique=True,index=True)  # 名字 admin -> 12345
    username = db.Column(db.String(10))
    passwd_hash = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    addr = db.Column(db.String(128))
    r_time = db.Column(db.DateTime,default=datetime.datetime.now)

    def set_password(self,passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def vary_password(self,passwd):
        return check_password_hash(self.passwd_hash,passwd)

class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

class Guestbook(db.Model):  # 表名将会是 movie
    __tablename__ = 'guestbook'
    id = db.Column(db.Integer, primary_key=True,auto_increment=True)  # 主键
    name = db.Column(db.String(60))
    msg = db.Column(db.String(100))
    c_time = db.Column(db.DateTime,default=datetime.datetime.now)
    r_ip =db.Column(db.String(20))

class Test(db.Model):  # 表名将会是 movie
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True,auto_increment=True)  # 主键
    name = db.Column(db.String(60))
    c_time = db.Column(db.DateTime,default=datetime.datetime.now)

