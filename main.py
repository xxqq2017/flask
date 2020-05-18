from flask import Flask, render_template

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'


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
    {'title': 'WALL-E', 'year': '2008','editor':'liujing'},
    {'title': 'The Pork of Music', 'year': '2012','editor':'张艺'},
    {'title': '活着', 'year': '1992','editor':'张艺谋'}
]

if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)