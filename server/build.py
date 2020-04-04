import random
from collections import defaultdict

from server.daily_doubles import handle_daily_doubles

def build_clue(clue, game_round=None):
  # clue => namedtuple
  # game_round => enum ('J', 'DJ', 'FJ', 'TB')

  clue_dict = {}

  clue_dict['value'] = clue.value
  clue_dict['answer'] = clue.answer
  clue_dict['question'] = clue.question
  clue_dict['is_daily_double'] = clue.is_daily_double
  clue_dict['invalid'] = clue.invalid

  if game_round and clue.round in ('J', 'DJ') and clue.round != game_round:
    # For a random game, adjust clue value if the round in the db is different than the round the clue will appear in.
    clue_dict['value'] = int(clue_dict['value'] / 2) if game_round == 'J' else clue_dict['value'] * 2

  return clue_dict

def build_category(clues, game_round=None):
  # clues => list of namedtuples
  # game_round => enum ('J', 'DJ', 'FJ', 'TB')

  category_dict = {
    'season': clues[0].season,
    'show_number': clues[0].show_number,
    'air_date': clues[0].air_date,
    'title': clues[0].category_title,
    'clues': defaultdict(str)
  }

  for clue in clues:
    category_dict['clues'][clue.id] = build_clue(clue, game_round)

  return category_dict

def build_random_board(clues):
  # Convert list of clues from random categories into a dictionary to be sent to client
  # clues => list of namedtuples

  board = defaultdict(lambda : defaultdict(lambda : {}))

  game_round = 'J'
  for i, clue in enumerate(clues):
    if i == 30:
      game_round = 'DJ'
    elif i == 60:
      game_round = 'FJ'

    if i % 5 == 0:
      board[game_round][clue.category_id] = build_category(clues[i:i+5], game_round)

  board = handle_daily_doubles(board)

  return board

def build_official_board(clues):
  # clues => list of namedtuples

  board = defaultdict(lambda : defaultdict(lambda : {}))
  categories_lookup = defaultdict(list)

  for clue in clues:
    categories_lookup[clue.category_id].append(clue)

  for category_id, clues in categories_lookup.items():
    board[clues[0].round][category_id] = build_category(clues)

  return board














