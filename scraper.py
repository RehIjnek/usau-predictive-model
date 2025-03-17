import requests
from bs4 import BeautifulSoup
import re

def scraper_helper(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html5lib')

    game_team_home = soup.find_all('span', attrs={'data-type': 'game-team-home'})
    game_team_away = soup.find_all('span', attrs={'data-type': 'game-team-away'})
    game_score_home = soup.find_all('span', attrs={'data-type': 'game-score-home'})
    game_score_away = soup.find_all('span', attrs={'data-type': 'game-score-away'})

    home_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_home]
    away_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_away]
    home_scores = [score.get_text() for score in game_score_home]
    away_scores = [score.get_text() for score in game_score_away]

    return home_teams, away_teams, home_scores, away_scores

def scraper(file_list):
    return