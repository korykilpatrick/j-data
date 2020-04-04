from collections import namedtuple

Clue = namedtuple('Clue', ['value', 'question', 'answer', 'category_id', 'official_game_id', 'is_daily_double', 'invalid', 'air_date'])
Category = namedtuple('Category', ['title', 'round', 'official_game_id'])
OfficialGame = namedtuple('OfficialGame', ['season', 'air_date', 'show_number', 'archive_id'])
User = namedtuple('User', ['username', 'password', 'permission'])