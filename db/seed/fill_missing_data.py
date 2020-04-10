
from db import DAL
from db.data_models.jeopardy import Clue, Category

dal = DAL()

def get_round_values(game_round):
  if game_round == 'J':
    return [200, 400, 600, 800, 1000]
  elif game_round == 'DJ':
    return [400, 800, 1200, 1600, 2000]
  elif game_round == 'FJ':
    return [5000]
  elif game_round == 'TB':
    return [5000]

def create_missing_categories():
  official_games = dal.execute('select count(*) as count, og.id as og_id from official_game og join category cat on cat.official_game_id=og.id group by og_id having count(*) < 13')

  inserts = []
  for og in official_games:
    j_cat_count = 0
    dj_cat_count = 0
    fj_cat_count = 0
    for cat in dal.execute('select * from category where official_game_id=%s', (og.og_id,),):
      if cat.round == 'J':
        j_cat_count += 1
      elif cat.round == 'DJ':
        dj_cat_count += 1
      elif cat.round == 'FJ':
        fj_cat_count += 1

    while j_cat_count < 6:
      inserts.append(Category('', 'J', og.og_id))
      j_cat_count += 1
    while dj_cat_count < 6:
      inserts.append(Category('', 'DJ', og.og_id))
      dj_cat_count += 1 
    if fj_cat_count < 1:
      inserts.append(Category('', 'FJ', og.og_id))

  dal.execute('insert into category (title, round, official_game_id) values (%s, %s, %s)', inserts, insert=True, many=True)
  print(f"Inserted {len(inserts)} blank categories.")


def fill_incomplete_categories():
  incomplete_cats = [(c.cat_id, c.count) for c in dal.execute('select count(*) as count, cat.id as cat_id from category cat join clue on cat.id=clue.category_id group by cat.id having count(*) < 5')]

  inserts = []
  for cat_id, num_missing in incomplete_cats:
    clues = dal.execute('select cat.round, clue.* from clue join category cat on clue.category_id=cat.id where cat.id=%s', (cat_id, )) or dal.execute('select  ')

    round_vals = get_round_values(clues[0].round)

    for val in [c.value for c in clues]:
      round_vals.remove(int(val))

    for val in round_vals:
      inserts.append(Clue(int(val), '', '', cat_id, clues[0].official_game_id, 0, 1, clues[0].air_date))


  dal.execute('insert into clue (value, question, answer, category_id, official_game_id, is_daily_double, invalid, air_date) values (%s, %s, %s, %s, %s, %s, %s, %s)', inserts, insert=True, many=True)
  print(f"Inserted {len(inserts)} clues from incomplete categories.")


def fill_empty_categories():
  empty_cats = dal.execute('select og.air_date, cat.* from category cat join official_game og on cat.official_game_id=og.id where not exists (select 1 from clue where category_id=cat.id)')

  inserts = []
  for cat in empty_cats:
    for val in get_round_values(cat.round):
      inserts.append(Clue(val, '', '', cat.id, cat.official_game_id, 0, 1, cat.air_date))

  dal.execute('insert into clue (value, question, answer, category_id, official_game_id, is_daily_double, invalid, air_date) values (%s, %s, %s, %s, %s, %s, %s, %s)', inserts, insert=True, many=True)
  print(f"Inserted {len(inserts)} clues from empty categories.")

def fill_missing_data():
  create_missing_categories()
  fill_incomplete_categories()
  fill_empty_categories()



if __name__ == '__main__':
  fill_missing_data()