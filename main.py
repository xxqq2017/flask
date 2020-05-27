from flask import Flask, render_template, request, flash, redirect,url_for
import os, sys, pymysql,time
from flask_login import LoginManager,login_user,logout_user,login_required,UserMixin,current_user
from flask_sqlalchemy import SQLAlchemy #数据库类导入
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
app.config['SECRET_KEY']='nihao'
# app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2468QAZwsx@@43.255.231.253:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


class User(db.Model,UserMixin):  # 表名将会是 user（自动生成，小写处理）
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20),unique=True,index=True)  # 名字 admin -> 12345
    username = db.Column(db.String(10))
    passwd_hash = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    addr = db.Column(db.String(128))


    def set_password(self,passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def vary_password(self,passwd):
        return check_password_hash(self.passwd_hash,passwd)

class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if not username or not password :
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.vary_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        addr = request.form['addr']
        if not username or not password1 or not password2:
            flash('Invalid input.')
            return redirect(url_for('register'))
        if password1 != password2:
            flash('passwd is not match!.')
            return redirect(url_for('register'))

        user2 = User.query.filter_by(username='%s'%username).first()
        email2 =User.query.filter_by(email='%s'%email).first()
        print(username,user2,email,email2)
        if user2.username == username or email2.email == email:
            flash('has exeist!')
            return redirect(url_for('register'))
        # 验证用户名和密码是否一致
        User.set_passwd(password1)

        login_user(user)  # 登入用户
        flash('Register success.')
        return redirect(url_for('register'))  # 重定向回登录页面

    return render_template('register.html')

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页

@app.route('/', methods=['GET', 'POST'])
def index():
    #user = User.query.first()
    #movies = Movie.query.all()
    # 传递的页码数量
    page = int(request.args.get('page') or 1)
    per_page = 5  # 每页数量
    #pagination = Movie.query.paginate(page, per_page, error_out=False) # 创建分页器对象

    pagination = Movie.query.order_by(Movie.id.desc()).paginate(page, per_page, error_out=False)
    movies = pagination.items
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
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
    return render_template('index.html', movies=movies,pagination=pagination)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        addr = request.form['addr']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        user = User.query.first()

        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        user.email = email
        user.addr = addr
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
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
    return render_template('edit.html', movie_id=movie_id, movie=movie) # 传入被编辑的电影记录


@app.route('/movie/delete/<movie_id>', methods=['POST','GET'])  # 限定只接受 POST 请求
@login_required
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
    return render_template('delete.html',movie=movie,movie_id=movie_id)

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


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)
