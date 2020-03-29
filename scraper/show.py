import requests
from bs4 import BeautifulSoup
import sys, os
from collections import defaultdict, namedtuple
from termcolor import cprint
import time

sys.path.insert(0, os.getcwd())

from scraper.validators import validate_clues, validate_categories, validate_round
from utils import write_to_file

def get_show_data(url):
  # Url => e.g. http://www.j-archive.com/showgame.php?game_id={archive_id}
  archive_id = int(url.split('=')[-1])

  try:
    response = requests.get(url).content.decode()
  except requests.exceptions.ConnectionError:
    msg = f"Request to url {url} got a connection error. Retrying."
    write_to_file(msg, warn=True)
    time.sleep(5)
    return get_show_data(url)

  soup = BeautifulSoup(response, 'html.parser')

  title_text = soup.find('title').text
  air_date, show_number = parse_show_title(title_text)

  cprint(f"{air_date}", 'cyan', attrs=['bold'])
  cprint(f"Show #{show_number}", 'magenta', attrs=['bold'])

  # categories => list of dicts
  # categories_dict => For finding category title based on round and category idx, e.g. categoriesdict[<round>][<idx>] = <title>
  categories, categories_dict = get_categories(soup)

  # clues => list of dicts
  clues = get_clues(soup, categories_dict, archive_id)

  categories = validate_round(categories, clues)
  validate_categories(categories, clues)
  validate_clues(clues)

  return show_number, air_date, categories, clues

def parse_show_title(title_text):
  if 'aired' in title_text:
    air_date = title_text.split('aired')[1].strip()
  elif 'taped' in title_text:
    air_date = title_text.split('taped')[1].strip()
  else:
    raise Exception(f"Unknown title for archive_id {archive_id}")

  show_number = int(title_text.split('#')[1].split(',')[0])
  if 'pilot' in title_text.lower():
    show_number += 100000
  elif 'super' in title_text.lower():
    show_number += 200000
  elif 'the greatest' in title_text.lower():
    show_number += 300000

  return air_date, show_number

def get_categories(soup):
  categories_dict = defaultdict(lambda : {})
  categories = []
  category_tds = soup.find_all('td', {"class": 'category_name'})

  # These td's don't directly reference the round but they do always appear in the order of j->dj->fj, so we can do some index tracking to make sure the c is stored correctly since sometimes j-archive won't list the j round or dj round
  for i, category_td in enumerate(category_tds):
    category_title = category_td.text.replace('&amp;', '&')
    category = {'title': category_title}

    if i < 6:
      categories_dict['J'][i+1] = category_title
      category['round'] = 'J'
    elif i < 12 and len(category_tds) > 7:
      categories_dict['DJ'][i-5] = category_title
      category['round'] = 'DJ'
    elif i == 12 or i == len(category_tds) - 1 == 6:
      # Either 13th category, or 7th category and J or DJ rounds ommitted
      categories_dict['FJ'][1] = category_title
      category['round'] = 'FJ'
    elif i == 13:
      # Won't work correctly if j-archive lists tb rounds where there are not also j, dj, fj rounds
      categories_dict['TB'][1] = category_title
      category['round'] = 'TB'
    
    categories.append(category)

  
  return categories, categories_dict

def get_clues(soup, categories_dict, archive_id):
  clues = []
  for clue_td in soup.find_all('td', {"class": 'clue'}):
    # All clue info is in this clue td
    clue = {}
    clue_text = clue_td.find('td', {"class": 'clue_text'})
    if not clue_text:
      msg = f"Couldn't find clue_text td for archive_id {archive_id}"
      write_to_file(msg, warn=True)
      continue

    clue_id = clue_text.get('id')
    clue['question'] = clue_text.text
    clue['round'], clue['category_title'], clue['value'] = parse_clue_id(clue_id, categories_dict, archive_id)
    clue['answer'] = get_answer(soup, clue_td, clue['round'])
    clue['daily_double'] = 1 if clue_td.find('td', {"class": 'clue_value_daily_double'}) else 0

    clues.append(clue)

  return clues

def parse_clue_id(clue_id, categories_dict, archive_id):
  # clue_id: string
  # e.g. "clue_DJ_6_5" -> Double Jeopardy round, 6th category, 5th clue ($2000)

  parsed_id = clue_id.split('_')
  j_round = parsed_id[1].upper()
  category_idx = 1 if j_round in ['FJ', 'TB'] else int(parsed_id[2])

  if j_round == 'J':
    clue_idx = int(parsed_id[3])
    value = 200 * clue_idx
  elif j_round == 'DJ':
    # Category titles will be stored in J round instead of DJ round if j-archive lists the DJ round but not the J round for a show
    if len(categories_dict['DJ']) == 0:
      categories_dict['DJ'] = categories_dict['J']
      categories_dict['J'] = {} 
    clue_idx = int(parsed_id[3])
    value = 400 * clue_idx
  elif j_round in ['FJ', 'TB']:
    value = 5000 # Arbitrary 

  category_title = categories_dict[j_round][category_idx] 

  return j_round, category_title, value

def get_answer(soup, clue_td, round):
  # clue_td: beautiful soup object
  answer_el = clue_td.find('div')
  if answer_el:
    # J and DJ clues
    res_str = 'correct_response">'
  else:
    # FJ and TB clues. TB is also listed w/ class final_round
    final_tables = soup.find_all('table', {"class": 'final_round'})
    idx = 1 if round == 'TB' else 0
    answer_el = final_tables[idx].find('div')

    res_str = 'correct_response\\\">'

  ans_str = answer_el.get('onmouseover').split(res_str)[1].replace("<em>", "").replace("<i>", "")
  while ans_str[0] == '<':
    ans_str = ans_str.split('>')[1]
  answer = ans_str.split('<')[0].replace("\\\'", "\'")

  if not answer:
    raise Exception(f"No answer found: {answer_el.get('onmouseover')}")

  return answer









