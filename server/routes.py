from flask import jsonify

import db.data_models.jeopardy as jdm
from server import app, dal
from server.game_dict import build_random_game_dict, build_official_game_dict, build_category_dict

@app.route('/')
def hello_world():
  return 'Hello World'

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

