import os, sys

sys.path.insert(0, os.getcwd())

from db import DAL
from db.seed.seed_show import save_show_data
from scraper.season import get_show_urls

dal = DAL()

# SEASON = int(dal.execute('select * from code_values where value_code=%s', ('CurrentSeason',), one_or_none=True).value)
SEASON = 36

""" Run this function to get new shows from the current season into the db. Either put this script on a cronjob to run M-F, or allow it to be invoked from the website or something.
"""

def update_season(season=SEASON):
  saved_archive_ids = [og.archive_id for og in dal.execute('select * from official_game where season=%s', (season, ))]

  count = 0
  for url in get_show_urls(season):
    if int(url.split('=')[-1]) not in saved_archive_ids:
      count += 1
      save_show_data(url, season)

  return count

if __name__ == '__main__':
  update_season()