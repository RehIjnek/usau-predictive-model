from src.game_scraper import game_scraper
from src.url_scraper import url_scraper
from src.importer import import_urls
from src.exporter import export_games, export_wl, export_pd
from src.win_loss import win_loss
from src.point_differential import point_differential
from src.usau_ranker import populate_games, compute_team_rating

if __name__ == '__main__':
    # urls
    # file_list = url_scraper()

    # events, dates, games
    # file_list = import_urls('urls.csv')
    # for url in file_list:
    #     event_name, event_date, home_teams, away_teams, home_scores, away_scores = game_scraper(url)
    #     export_games(event_name, event_date, home_teams, away_teams, home_scores, away_scores)

    # team records
    # team_records = win_loss()
    # export_wl(team_records)

    # average point differentials, point differentials against top teams
    # team_stats = point_differential()
    # export_pd(team_stats)

    # usau elos
    games = populate_games()
    team_elos = compute_team_rating(games)
    for team, elo in team_elos.items():
        print(team, elo)