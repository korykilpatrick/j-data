from flask import jsonify

from server import app, dal
from server.game_dict import build_random_game_dict, build_official_game_dict, build_category_dict
import db.data_models.jeopardy as jdm

@app.route('/')
def hello_world():
  api_info = {
    '/game/og': 'get a random official game',
    '/game/random': 'get a random game',
    '/game/category': 'get a random category',
    '/game/clue/<round>': 'get a random clue by round (J, DJ, FJ, TB)'
  }

  return api_info

@app.route('/game/og', methods=['GET'])
def get_official_game():  
  # Next step let them pass optional parameters like show number, air_date, season
  clues = dal.callproc('get_official_game_clues')
  return build_official_game_dict(clues)

@app.route('/game/random')
def get_random_game():
  clues = dal.callproc('get_random_game_clues')
  return build_random_game_dict(clues)

@app.route('/game/category')
def get_random_category():
  # When a user wants to sub out a category
  clues = dal.callproc('get_random_category')
  return build_category_dict(clues)

@app.route('/game/clue/<game_round>', methods=['GET'])
def get_random_clue(game_round):
  tb_clue = dal.callproc('get_random_clue', (game_round, ), one_or_none=True)

  return build_category_dict([tb_clue])

