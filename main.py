from src.game_scraper import game_scraper
from src.url_scraper import url_scraper
from src.importer import import_data
from src.exporter import export_data

if __name__ == '__main__':
    file_list = url_scraper()
    home_teams, away_teams, home_scores, away_scores = game_scraper(file_list)
    export_data(home_teams, away_teams, home_scores, away_scores)