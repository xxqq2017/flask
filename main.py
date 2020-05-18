from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #数据库类导入
import os, sys

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

name = 'xiangqing'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988','editor':'jhon wang'},
    {'title': 'Dead Poets Society', 'year': '1989','editor':'jhon wang2'},
    {'title': 'A Perfect World', 'year': '1993','editor':'jhon wang2'},
    {'title': 'Leon', 'year': '1994','editor':'mark'},
    {'title': 'Mahjong', 'year': '1996','editor':'stphone'},
    {'title': 'Swallowtail Butterfly', 'year': '1996','editor':'ptell'},
    {'title': 'King of Comedy', 'year': '1999','editor':'xiangm'},
    {'title': 'Devils on the Doorstep', 'year': '1999','editor':'huaqiang'},
    {'title': 'WALL-E', 'year': '2008','editor':'巩俐'},
    {'title': 'The Pork of Music', 'year': '2012','editor':'刘德伟'},
    {'title': '活着', 'year': '1992','editor':'张艺谋'}
]

if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)