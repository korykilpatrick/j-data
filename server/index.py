from flask import Flask

from db import DAL 
import db.data_models.jeopardy as jdm
from server.convert import build_game_dict, build_official_game_dict

app = Flask(__name__)
dal = DAL()

@app.route('/game/og/'):
def get_official_game():  
  # To start, just grab a random game
  # Next step let them pass optional parameters like show number, air_date, season
  clues = dal.callproc('get_official_game_clues')
  return build_official_game_dict(clues)

@app.route('/game/random')
def get_random_game():
  # get J and DJ clues
  clues = dal.callproc('build_random_game')
  return build_random_game_dict(clues)

@app.route('/game/category')
def get_random_category():
  # When a user wants to sub out a category
  clues = dal.callproc('get_random_clues', (1, ))
  return 

@app.route('/game/random/<game_id>')
def get_tiebreaker():
  tb_clue = dal.callproc('get_random_clue', ('TB', ), one_or_none=True)

