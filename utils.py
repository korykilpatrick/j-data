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

def print_daily_doubles(game_dict):
  for game_round in ('J', 'DJ'):
    for category_id in game_dict[game_round]:
      for clue_id in game_dict[game_round][category_id]['clues']:
        if game_dict[game_round][category_id]['clues'][clue_id]['is_daily_double']:
          print(game_round, category_id, game_dict[game_round][category_id]['clues'][clue_id]['value'])

def print_game_dict(game_dict):
  for game_round in game_dict:
    cprint(f'\n{game_round} ROUND\n', 'magenta', attrs=['bold'])
    for category_id in game_dict[game_round]:
      cprint(f"Category: {game_dict[game_round][category_id]['title']}", 'magenta')
      for clue_id, clue_data in game_dict[game_round][category_id]['clues'].items():
        if clue_data.get('category_id', None) and clue_data['category_id']!= category_id:
          cprint(f"WE FUCKED UP {game_round}, {category_id}, {clue_data['category_id'], clue_id}", 'red')
        else:
          cprint(f"{clue_data['value']}", 'yellow' if not clue_data['is_daily_double'] else 'green')
          cprint(f"{clue_data['question']}", 'cyan' if not clue_data['is_daily_double'] else 'green')
          cprint(f"{clue_data['answer']}", 'blue' if not clue_data['is_daily_double'] else 'green', attrs=['bold'])





