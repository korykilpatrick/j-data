from flask import jsonify, request
from datetime import date
import requests
import random


from db.seed.update_season import update_season
from server import app, dal
from server.build import build_random_board, build_official_board, build_category

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
  params = request.args.to_dict()
  if not game_round:
    game_round = random.choice(['J', 'DJ', 'FJ', 'TB'])

  clue = dal.callproc('get_random_clue', (game_round, params.get('startDate', '1900-01-01'), params.get('endDate', date.today())))
  return build_category(clue)

@app.route('/category')
def get_random_category():
  params = request.args.to_dict()
  clues = dal.callproc('get_random_category', (params.get('startDate', '1900-01-01'), params.get('endDate', date.today())))
  return build_category(clues)

@app.route('/board')
@app.route('/board/official', methods=['GET'])
def get_official_board():  
  params = request.args.to_dict()
  clues = dal.callproc('get_official_board', (params.get('startDate', '1900-01-01'), params.get('endDate', date.today())))
  return build_official_board(clues)

@app.route('/board/random')
def get_random_board():
  params = request.args.to_dict()
  clues = dal.callproc('get_random_board', (params.get('startDate', '1900-01-01'), params.get('endDate', date.today())))
  return build_random_board(clues)

@app.route('/update/season')
def update_current_season():
  try:
    count = update_season()
    return f"Successfully added {count} games!" if count else "Current season already up to date!"
  except Exception as e:
    return e




