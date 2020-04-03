from flask import jsonify, redirect, url_for

import db.data_models.jeopardy as jdm
from server import app, dal

# @app.route('/', methods=['GET'])
# def home():
#   return 'home'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if g.user:
    return redirect(url_for('home'))

  user = dal.execute('select * from users where username=(%s)', args=(form.username.data, ), one_or_none=True)

  if user and user.password == password:
    session['user'] = user.username

  return 'login'