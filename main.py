from src.game_scraper import game_scraper
from src.url_scraper import url_scraper
from src.importer import import_urls
from src.exporter import export_games

if __name__ == '__main__':
    # scraper for new tournaments
    # file_list = url_scraper()

    file_list = import_urls('urls.csv')
    for url in file_list:
        event_name, home_teams, away_teams, home_scores, away_scores = game_scraper(url)
        export_games(event_name, home_teams, away_teams, home_scores, away_scores)