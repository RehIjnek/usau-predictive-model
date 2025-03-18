import requests
from bs4 import BeautifulSoup
import re
import time

def scraper_helper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    games = soup.find_all('span', attrs={'data-type': True})

    home_teams, away_teams, home_scores, away_scores = [], [], [], []

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

    return home_teams, away_teams, home_scores, away_scores

def game_scraper(file_list):
    home_teams, away_teams, home_scores, away_scores = [], [], [], []

    for url in file_list:
        temp1, temp2, temp3, temp4 = scraper_helper(url)
        home_teams.extend(temp1)
        away_teams.extend(temp2)
        home_scores.extend(temp3)
        away_scores.extend(temp4)
        time.sleep(3)

    return home_teams, away_teams, home_scores, away_scores