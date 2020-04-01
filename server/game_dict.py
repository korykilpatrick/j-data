import random
from collections import defaultdict

from server.daily_doubles import handle_daily_doubles

def build_clue_dict(clue, game_round=None):
  clue_dict = {}
  for key, val in clue._asdict().items():
    if key in ('value', 'question', 'answer', 'is_daily_double'):
      clue_dict[key] = val

  if game_round and clue.round in ('J', 'DJ') and clue.round != game_round:
    clue_dict['value'] = int(clue_dict['value'] / 2) if game_round == 'J' else clue_dict['value'] * 2

  return clue_dict

def build_category_dict(clues, game_round):
  category_dict = {
    'season': clues[0].season,
    'show_number': clues[0].show_number,
    'air_date': clues[0].air_date,
    'title': clues[0].category_title,
    'clues': defaultdict(str)
  }

  for clue in clues:
    category_dict['clues'][clue.id] = build_clue_dict(clue, game_round)

  return category_dict

def build_game_dict(clues):
  # convert list of clues from db into a dictionary to be sent to client
  game_dict = defaultdict(lambda : defaultdict(lambda : {}))

  game_round = 'J'
  for i, clue in enumerate(clues):
    if i == 30:
      game_round = 'DJ'
    elif i == 60:
      game_round = 'FJ'

    if i % 5 == 0:
      game_dict[game_round][clue.category_id] = build_category_dict(clues[i:i+5], game_round)

  game_dict = handle_daily_doubles(game_dict)

  return game_dict
