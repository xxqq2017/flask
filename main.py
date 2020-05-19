from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy #数据库类导入
import os, sys
import pymysql


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

@app.route('/')
def index():
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='liutuwang',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT username,email,user_pass FROM cdb_user where email != '' limit 100"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('index.html',movies=u)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.context_processor
def t_context():
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='liutuwang',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT username FROM cdb_user where email != '' limit 1"
    cur.execute(sql)
    names = cur.fetchone()
    conn.close()
    return dict(name=names[0])

#name = 'xiangqing'
names={'name':'xiangqing'}


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)