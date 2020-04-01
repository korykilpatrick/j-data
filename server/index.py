from flask import Flask

from db import DAL 
import db.data_models.jeopardy as jdm
from server.convert import build_game_dict

app = Flask(__name__)
dal = DAL()

@app.route('/'):
def get_clues():  
  # can return dictionary and it will be auto jsonified by flask

  dal.execute('select * from clues where category_id=%s', (category.id))

  dal.callproc('get_official_game_clues')

def get_random_game():
  # get J and DJ clues
  clues = dal.callproc('build_random_game')
  return build_game_dict(clues)

def get_tiebreaker():
  tb_clue = dal.callproc('get_random_clue', ('TB', ), one_or_none=True)

