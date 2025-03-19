import requests
from bs4 import BeautifulSoup
import re
import time

def game_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    games = soup.find_all('span', attrs={'data-type': True})

    home_teams, away_teams, home_scores, away_scores = [], [], [], []

    match = re.search(r"/events/([^/]+)/", url)
    event_name = match.group(1)

    for game in games:
        data_type = game['data-type']
        text = game.get_text(strip=True)

        if data_type == "game-team-home":
            home_teams.append(re.sub(r'\([^)]*\)\s*$', '', text).strip())
        elif data_type == "game-team-away":
            away_teams.append(re.sub(r'\([^)]*\)\s*$', '', text).strip())
        elif data_type == "game-score-home":
            home_scores.append(text)
        elif data_type == "game-score-away":
            away_scores.append(text)

    return event_name, home_teams, away_teams, home_scores, away_scores