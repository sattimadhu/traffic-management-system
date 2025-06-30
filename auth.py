# auth.py
from flask import session, redirect, url_for

def login_user(username, password):
    if username == 'madhu' and password == '2004':
        session['user'] = username
        return True
    return False

def logout_user():
    session.pop('user', None)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap