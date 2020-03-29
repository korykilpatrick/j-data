import requests
from bs4 import BeautifulSoup

def get_show_urls(season):
  res = requests.get(f"http://www.j-archive.com/showseason.php?season={season}").content.decode()
  soup = BeautifulSoup(res, 'html.parser')

  show_urls = [a.get('href') for a in soup.find_all('a') if 'www.j-archive.com/showgame.php?game_id=' in a.get('href')]
  # Shows returned in reverse order on j-archive    
  show_urls.reverse()

  return show_urls



