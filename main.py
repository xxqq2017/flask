from flask import Flask, render_template, request, flash, redirect,url_for
import config
import os, sys, pymysql
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy #数据库类导入

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'
# app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控
# db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app



@app.route('/', methods=['GET', 'POST'])
def index():
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='test',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM movie"
    cur.execute(sql)
    movies = cur.fetchall()
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        id = request.form.get('id')
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or not id or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        sql_update="insert into movie (id,title,year) values(%s,%s,%s)"%(id,title,year)
        cur.execute(sql_update)
        conn.commit()  # 提交数据库会话
        conn.close()
        flash('Item created.')  # 显示成功创建的提示
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='test',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM movie where id =%s"%movie_id
    cur.execute(sql)
    movies = cur.fetchone()
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        sql2 = "update movie set title=%s ,year = %s where id=%s" %(title,year,movie_id)
        cur.execute(sql2)
        conn.commit()
        conn.close() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    #return render_template(url_for('edit', movie_id=movie_id,movie=movies)) # 传入被编辑的电影记录
    return render_template('edit.html', movie=movies) # 传入被编辑的电影记录


@app.route('/movie/delete/<movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='test',
                           charset='utf8')
    cur = conn.cursor()
    sql_delete = "delete FROM movie where id=%s"%movie_id
    cur.execute(sql_delete)
    conn.commit()
    flash('Item deleted.')
    return render_template(url_for('index'))  # 重定向回主页

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        UPLOAD_FOLDER = 'c:\data\project\env'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
        f.save(UPLOAD_FOLDER/f.filename)
        flash('file uploaded successfully')
        return render_template('upload.html')
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.context_processor
def t_context():
    conn = pymysql.connect(host='43.255.231.253', user='root',
                           password='2468QAZwsx@', db='test',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user"
    cur.execute(sql)
    names = cur.fetchone()
    conn.close()
    return dict(name=names[1])

#name = 'xiangqing'
names={'name':'xiangqing'}


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)
