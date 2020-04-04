import random

def handle_daily_doubles(board, dd_lookup={'J': 1, 'DJ': 2}):
  # Right now the get_random_game_clues stored procedure doesn't handle daily doubles, which means there could be anywhere between 0 and 6 daily doubles in a round.
  # dd_lookup => dict w/ number of daily doubles per round (1-6). Not used for now, but potential future variant could involve setting the number of daily doubles in a round

  for game_round in ('J', 'DJ'):
    daily_doubles = []
    for category_id in board[game_round]:
      for clue_id in board[game_round][category_id]['clues']:
        if board[game_round][category_id]['clues'][clue_id]['is_daily_double']:
          daily_doubles.append((category_id, clue_id))

    num_dds = dd_lookup[game_round]
    if len(daily_doubles) < num_dds:
      board = add_daily_doubles(board, game_round, daily_doubles, num_dds)
    elif len(daily_doubles) > num_dds:
      board = remove_daily_doubles(board, game_round, daily_doubles, num_dds)

  return board

def remove_daily_doubles(board, game_round, daily_doubles, num_dds):
  # game_round => 'J', 'DJ'
  # daily_doubles => list, [(<category_id>, <clue_id>)...
  # num_dds => int, the desired number of daily doubles

  keep = random.sample(daily_doubles, num_dds)
  for clue in daily_doubles:
    if clue not in keep:
      category_id, clue_id = clue
      board[game_round][category_id]['clues'][clue_id]['is_daily_double'] = 0

  return board

def add_daily_doubles(board, game_round, daily_doubles, num_dds):
  # game_round => 'J', 'DJ'
  # daily_doubles => list, [(<category_id>, <clue_id>)...
  # num_dds => int, the desired number of daily doubles
  
  while len(daily_doubles) < num_dds:
    category_id = list(board[game_round])[random.randint(0, 5)]
    if len(daily_doubles):
      # Set up to handle potential variant of 1 DD per category
      while category_id in [f[0] for f in daily_doubles]:
        category_id = list(board[game_round])[random.randint(0, 5)]

    clue_id = list(board[game_round][category_id]['clues'])[random.randint(1, 4)]

    board[game_round][category_id]['clues'][clue_id]['is_daily_double'] = 1
    daily_doubles.append((category_id, clue_id))

  return board