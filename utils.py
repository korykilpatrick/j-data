from termcolor import cprint

def write_to_file(msg, err=False, warn=False, out=False):
  if err:
    color = 'red'
    filename = "stderr.log"
  elif warn:
    color = 'yellow'
    filename = 'stdwarn.log'
  elif out:
    color = 'magenta'
    filename = 'stdout.log'

  cprint(msg, color, attrs=['bold'])
  f = open('logs/' + filename, "a")
  f.write(msg + '\n')
  f.close()

def print_daily_doubles(board):
  for game_round in ('J', 'DJ'):
    for category_id in board[game_round]:
      for clue_id in board[game_round][category_id]['clues']:
        if board[game_round][category_id]['clues'][clue_id]['is_daily_double']:
          print(game_round, category_id, board[game_round][category_id]['clues'][clue_id]['value'])

def print_board(board):
  for game_round in board:
    cprint(f'\n{game_round} ROUND\n', 'magenta', attrs=['bold'])
    for category_id in board[game_round]:
      cprint(f"Category: {board[game_round][category_id]['title']}", 'magenta')
      for clue_id, clue_data in board[game_round][category_id]['clues'].items():
        if clue_data.get('category_id', None) and clue_data['category_id']!= category_id:
          cprint(f"WE FUCKED UP {game_round}, {category_id}, {clue_data['category_id'], clue_id}", 'red')
        else:
          cprint(f"{clue_data['value']}", 'yellow' if not clue_data['is_daily_double'] else 'green')
          cprint(f"{clue_data['question']}", 'cyan' if not clue_data['is_daily_double'] else 'green')
          cprint(f"{clue_data['answer']}", 'blue' if not clue_data['is_daily_double'] else 'green', attrs=['bold'])


# def print_random_game():
#   dal = DAL()
#   clues = dal.callproc('get_random_board')
#   board = build_random_board(clues)
#   print_board(board)
#   print_daily_doubles(board)

# def print_official_game():
#   dal = DAL()
#   clues = dal.callproc('get_official_board')
#   board = build_official_board(clues)
#   print_board(board)
#   print_daily_doubles(board)





