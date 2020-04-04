import os, sys
from collections import defaultdict
from termcolor import cprint
import time

sys.path.insert(0, os.getcwd())

from db import DAL
from db.data_models.jeopardy import Clue, Category
from scraper.show import get_show_data

ARCHIVE_ID = 3576
dal = DAL()

def get_category_dict(official_game_id):
  categories = dal.execute('select * from category where official_game_id=%s', (official_game_id, ))

  category_dict = defaultdict(lambda : defaultdict(int))
  for cat in categories:
    category_dict[cat.round][cat.title] = cat.id

  return category_dict

def insert_categories(categories, official_game_id, air_date):
  inserts = []
  for cat in categories:
    inserts.append(Category(cat['title'], cat['round'], official_game_id))

  dal.execute('insert into category (title, round, official_game_id) values (%s, %s, %s)', inserts, many=True, insert=True)

def insert_new_clues(clues, category_dict, air_date, official_game_id):
  
  inserts = []
  for clue in clues:
    category_id = category_dict[clue['round']][clue['category_title']]
    inserts.append(Clue(clue['value'], clue['question'], clue['answer'], category_id, official_game_id, clue['daily_double'], 0, air_date))
  
  dal.execute('insert into clue (value, question, answer, category_id, official_game_id, is_daily_double, invalid, air_date) values (%s, %s, %s, %s, %s, %s, %s, %s)', inserts, many=True, insert=True)

def insert_official_game(season, air_date, show_number, archive_id):
  dal.execute('insert into official_game (season, air_date, show_number, archive_id) values (%s, %s, %s, %s)', (season, air_date, show_number, archive_id, ), insert=True)

  return dal.execute('select * from official_game where air_date=%s and show_number=%s', ( air_date, show_number, ), one_or_none=True).id

def save_show_data(url, season=None):
  # url => url of show data
 
  archive_id = url.split('=')[-1]
  show_number, air_date, categories, clues = get_show_data(url)
  if not show_number:
    raise Exception(f"Unable to find show_number for archive_id: {archive_id}")
  official_game_id = insert_official_game(season, air_date, show_number, archive_id)

  insert_categories(categories, official_game_id, air_date)
  cprint(f"Inserted {len(categories)} categories.", 'green')

  category_dict = get_category_dict(official_game_id)

  insert_new_clues(clues, category_dict, air_date, official_game_id)
  cprint(f"Inserted {len(clues)} clues.", 'green')


def main(archive_id):
  url = f"http://www.j-archive.com/showgame.php?game_id={archive_id}"
  save_show_data(url)

if __name__ == '__main__':
  # allow for command line arg to get archive_id?
  main(ARCHIVE_ID)


