from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm,Form
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<int:name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)