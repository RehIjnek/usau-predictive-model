from scraper import scraper
from importer import import_data
from exporter import export_data

if __name__ == '__main__':
    file_list = import_data('urls.csv')
    home_teams, away_teams, home_scores, away_scores = scraper(file_list)
    export_data(home_teams, away_teams, home_scores, away_scores)