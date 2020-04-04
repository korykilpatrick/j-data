from flask import jsonify
import random

from server import app, dal
from server.board import build_random_board, build_official_board, build_category
import db.data_models.jeopardy as jdm

@app.route('/')
def hello_world():
  return {
    '/clue': 'get a random clue',
    '/clue/<round>': 'get a random clue by round (J, DJ, FJ, TB)',
    '/category': 'get a random category',
    '/board/random': 'get a random board',
    '/board/official': 'get a random official game board',
  }

@app.route('/clue')
@app.route('/clue/<game_round>', methods=['GET'])
def get_random_clue(game_round=None):
  if not game_round:
    game_round = random.choice(['J', 'DJ', 'FJ', 'TB'])

  clue = dal.callproc('get_random_clue', (game_round, ), one_or_none=True)
  return build_category([clue])

@app.route('/board/official', methods=['GET'])
def get_official_board():  
  # Next step let them pass optional parameters like show number, air_date, season
  clues = dal.callproc('get_official_board')
  return build_official_board(clues)

@app.route('/board/random')
def get_random_board():
  clues = dal.callproc('get_random_board')
  return build_random_board(clues)

@app.route('/category')
def get_random_category():
  clues = dal.callproc('get_random_category')
  return build_category(clues)


