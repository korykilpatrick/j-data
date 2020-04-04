import sys, os
from termcolor import cprint

sys.path.insert(0, os.getcwd())

from TechnousDB.DAL import DAL

dal = DAL()

# 11,304 clues were missing from the gameboard on j-archive

cprint(f"Show count: {dal.execute('select count(*) as c from official_game')[0].c}", 'yellow')
cprint(f"Category count: {dal.execute('select count(*) as c from category')[0].c}", 'cyan')
cprint(f"Clue count: {dal.execute('select count(*) as c from clue')[0].c}", 'magenta')