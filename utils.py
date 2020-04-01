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





