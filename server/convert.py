import random
from collections import defaultdict

def game_clue_to_dict(clue, game_round=None):
  clue_dict = {}
  for key, val in clue._asdict().items():
    if key in ('value', 'question', 'answer', 'is_daily_double'):
      clue_dict[key] = val

  if game_round and clue.round != game_round and clue.round in ('J', 'DJ'):
    clue_dict['value'] = clue_dict['value'] * 2 if game_round == 'DJ' else int(clue_dict['value'] / 2)

  return clue_dict

def handle_daily_doubles(game_dict, target=None):
  # Right now the get_random_game_clues stored procedure doesn't handle daily doubles, which means there could be anywhere between 0 and 6 daily doubles in a round.
  # target => int (1-6). Not used for now, but potential future variant could involve setting the number of daily doubles in a round
  if target > 6:
    raise Exception(f"Target of {target} passed in to handle_daily_doubles is great than max allowed of 6.")

  for game_round in ('J', 'DJ'):
    daily_doubles = []
    for category_id in game_dict[game_round]:
      for clue_id in game_dict[game_round][category_id]['clues']:
        if game_dict[game_round][category_id]['clues'][clue_id]['is_daily_double']:
          daily_doubles.append((category_id, clue_id))

    target = target or (1 if game_round == 'J' else 2)
    while len(daily_doubles) < target:
      category_idx = random.randint(0, 5)
      if len(daily_doubles):
        # Set up to handle potential variant of 1 DD per category
        category_id = list(game_dict[game_round])[category_idx]
        while category_id in [f[0] for f in daily_doubles]:
          category_idx = random.randint(0, 5)
          category_id = list(game_dict[game_round])[category_idx]

      clue_idx = random.randint(1, 4)
      clue_id = list(game_dict[game_round][category_id]['clues'])[clue_idx]

      game_dict[game_round][category_id]['clues'][clue_id]['is_daily_double'] = 1
      daily_doubles.append((category_id, clue_id))

    if len(daily_doubles) > target:
      keep = random.sample(daily_doubles, target)
      for clue in daily_doubles:
        if clue not in keep:
          category_id, clue_id = clue
          game_dict[game_round][category_id]['clues'][clue_id]['is_daily_double'] = 0

  return game_dict

def build_game_dict(clues):
  # convert list of clues from db into a dictionary to be sent to client
  game_dict = defaultdict(lambda : defaultdict(lambda : {}))
  for i, clue in enumerate(clues):
    if i < 30:
      game_round = 'J'
    elif i < 60:
      game_round = 'DJ'
    else:
      game_round = 'FJ'

    if i % 5 == 0:
      # Add category metadata
      game_dict[game_round][clue.category_id]['season'] = clue.season
      game_dict[game_round][clue.category_id]['show_number'] = clue.show_number
      game_dict[game_round][clue.category_id]['air_date'] = clue.air_date
      game_dict[game_round][clue.category_id]['title'] = clue.category_title
      game_dict[game_round][clue.category_id]['clues'] = defaultdict(str)

    game_dict[game_round][clue.category_id]['clues'][clue.id] = game_clue_to_dict(clue, game_round)

  game_dict = handle_daily_doubles(game_dict)

  return game_dict