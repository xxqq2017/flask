from flask import Flask, render_template, request, flash, redirect,url_for
import os, sys, pymysql
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy #数据库类导入

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'
# app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2468QAZwsx@@43.255.231.253:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.first()
    movies = Movie.query.all()
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        #id = request.form.get('id')
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        m1 = Movie(title=title,year=year)
        db.session.add(m1)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))
    return render_template('index.html', movies=movies, user=user)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    user = User.query.first()
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        m1=Movie.query.get(movie_id)
        m1.title = title
        m1.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie_id=movie_id, movie=movie,user=user) # 传入被编辑的电影记录


@app.route('/movie/delete/<movie_id>', methods=['POST','GET'])  # 限定只接受 POST 请求
def delete(movie_id):
    user = User.query.first()
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        user = User.query.first()
        movie = Movie.query.get_or_404(movie_id)
        m_d = Movie.query.get(movie_id)
        db.session.delete(m_d)
        db.session.commit()
        flash('Item deleted.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('delete.html',movie=movie,user=user,movie_id=movie_id)

@app.route('/upload',methods=['POST','GET'])
def upload():
    user = User.query.first()
    if request.method == 'POST':
        f = request.files['file']
        UPLOAD_FOLDER = 'c:\data\project\env'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
        f.save(UPLOAD_FOLDER/f.filename)
        flash('file uploaded successfully')
        return render_template('upload.html')
    return render_template('upload.html',user=user)

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

# #name = 'xiangqing'
# names={'name':'xiangqing'}


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)
