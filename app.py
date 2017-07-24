from flask import Flask, g, redirect, render_template, \
 request, session, url_for
from functools import wraps
import psycopg2

# Configuration
DATABASE = 'ezbuy.db'
SECRET_KEY = '''\xad\x91\xd0%It\xa4h
\xe6%\x89\x05b\xc7X\xbc\x08\x12[\xba\xb7\x91f\x12'''
USERNAME = 'admin'
PASSWORD = 'admin'


app = Flask(__name__)

app.config.from_object(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user')
@login_required
def user_home():
    return render_template('user.html')


@app.route('/processor')
@login_required
def user_processor():
    return render_template('processor.html')


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/product')
def product():
    return render_template('production.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USER'] \
        or request.form['password'] != app.config['PASSWORD']:
            error = 'Incorrect username/password combination.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error), status_code


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
           flash('Login Required')
            return redirect(url_for('login'))
    return wrap 


def connect_db():
    return psycopg2.connect(app.config['DATABASE'])


if __name__ == '__main__':
    app.run(debug=True)
