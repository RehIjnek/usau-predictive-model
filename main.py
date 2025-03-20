from src.game_scraper import game_scraper
from src.url_scraper import url_scraper
from src.importer import import_urls
from src.exporter import export_games

if __name__ == '__main__':
    # url scraper for new tournaments
    # file_list = url_scraper()

    # for testing
    # file_list = ['https://play.usaultimate.org/events/Smoky-Mountain-Invite-2025/schedule/Men/CollegeMen/',
    #              'https://play.usaultimate.org/events/Florida-Warm-Up-2025/schedule/Men/CollegeMen/',
    #              'https://play.usaultimate.org/events/Carolina-Kickoff-mens-2025/schedule/Men/CollegeMen/']

    file_list = import_urls('urls.csv')
    for url in file_list:
        event_name, event_date, home_teams, away_teams, home_scores, away_scores = game_scraper(url)
        export_games(event_name, event_date, home_teams, away_teams, home_scores, away_scores)