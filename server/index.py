from flask import Flask


from db import DAL 
import db.data_models.jeopardy as jdm

app = Flask(__name__)

@app.route('/'):
def get_clues():  
  # can return dictionary and it will be auto jsonified by flask
  dal.execute('select * from category order by title')

  dal.execute('select * from clues where category_id=%s', (category.id))

  dal.callproc('get_official_game_clues')