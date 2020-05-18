from flask import Flask, render_template

app=Flask(__name__)
app.config['SECRET_KEY']='nihao'


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='192.168.50.222',port=80, debug=True)