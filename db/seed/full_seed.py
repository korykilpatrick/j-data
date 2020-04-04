import sys, os
from datetime import datetime
from termcolor import cprint

sys.path.insert(0, os.getcwd())
from scraper.season import get_show_urls
from seed.seed_show import save_show_data
from utils import write_to_file

SEASONS = [str(n) for n in range(1, 37)] + ['trebekpilots', 'superjeopardy', 'goattournament']

def full_seed():
  start_time = datetime.now()
  for season in SEASONS:
    write_to_file(f'SAVING SEASON {season}', out=True)
    for url in get_show_urls(season):
      save_show_data(url, season)

  end_time = datetime.now()
  cprint(f"Seed complete! Time: {str(end_time - start_time)}", 'green', attrs=['bold'])


if __name__ == '__main__':
  full_seed()
