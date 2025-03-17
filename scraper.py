# usau scraper
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

def pool_scraper(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html5lib')

    game_number = soup.find_all('tr', attrs={'data-game': True})
    game_team_home = soup.find_all('span', attrs={'data-type': 'game-team-home'})
    game_team_away = soup.find_all('span', attrs={'data-type': 'game-team-away'})
    game_score_home = soup.find_all('span', attrs={'data-type': 'game-score-home'})
    game_score_away = soup.find_all('span', attrs={'data-type': 'game-score-away'})

    games = [tr['data-game'] for tr in game_number]
    home_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_home]
    away_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_away]
    home_scores = [score.get_text() for score in game_score_home]
    away_scores = [score.get_text() for score in game_score_away]

    return games, home_teams, away_teams, home_scores, away_scores

def bracket_scraper(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html5lib')

    game_number = soup.find_all('tr', attrs={'data-game': True})
    game_team_home = soup.find_all('span', attrs={'data-type': 'game-team-home'})
    game_team_away = soup.find_all('span', attrs={'data-type': 'game-team-away'})
    game_score_home = soup.find_all('span', attrs={'data-type': 'game-score-home'})
    game_score_away = soup.find_all('span', attrs={'data-type': 'game-score-away'})

    games = [tr['data-game'] for tr in game_number]
    home_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_home]
    away_teams = [re.sub(r'\([^)]*\)\s*$', '', team.get_text().strip()).strip() for team in game_team_away]
    home_scores = [score.get_text() for score in game_score_home]
    away_scores = [score.get_text() for score in game_score_away]

    return games, home_teams, away_teams, home_scores, away_scores
    
def export_data(games, home_teams, away_teams, home_scores, away_scores):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']
    
    for i in range(len(games)):
        document = {
            'game' : games[i],
            'home_team' : home_teams[i],
            'away_team' : away_teams[i],
            'home_score' : home_scores[i],
            'away_score' : away_scores[i]
        }
        collection.insert_one(document)
        
def import_urls(file_name)

if __name__ == '__main__':
    url = 'https://play.usaultimate.org/events/The-Lobster-Pot-2024/schedule/Men/CollegeMen/lower/'
    games, home_teams, away_teams, home_scores, away_scores = scraper(url)
    export_data(games, home_teams, away_teams, home_scores, away_scores)