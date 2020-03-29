def validate_categories(categories, clues):
  if len(categories) not in [0, 6, 7, 12, 13, 14]:
    raise Exception(f"Only found {len(categories)} categories")

  for i, cat in enumerate(categories):
    if not cat['title']:
      raise Exception(f"Category {i} has no title.")

def validate_clues(clues):
  for i, clue in enumerate(clues):
    if not clue['question']:
      raise Exception(f"Clue {clue['value']} in category {clue['category_title']} has no question")
    if not clue['answer']:
      raise Exception(f"Clue {clue['value']} in category {clue['category_title']} has no answer")
    if not clue['category_title']:
      raise Exception(f"Clue {clue['value']} with question {clue['question']} has no category title")

def validate_round(categories, clues):
  # If DJ round is listed but J round isn't then categories will be stored with round of 'J' while clues will be stored with round of 'DJ'
  
  if len(categories) == 6 or len(categories) == 7:
    if categories[0]['round'] == 'J' and clues[0]['round'] == 'DJ':
      for category in categories:
        if category['round'] == 'J':
          category['round'] = 'DJ'

  return categories
