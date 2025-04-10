# chatgpt generated, tweaked by Kenji Her
# need to figure out data strucs for parameters + fixing iterator

import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from datetime import datetime

def calculate_game_rating(opponent_rating: float, win: bool, winning_score: int, losing_score: int):
    """Computes game rating based on opponent rating and score differential."""
    x = compute_score_differential(winning_score, losing_score)
    return opponent_rating + x if win else opponent_rating - x

def compute_score_differential(winning_score: int, losing_score: int):
    """Computes the rating differential x based on the score."""
    score_diff = winning_score - losing_score
    
    if score_diff == 1:
        return 125
    elif winning_score > 2 * losing_score:
        return 600
    else:
        r = losing_score / (winning_score - 1)
        return int(125 + 475 * ((np.sin(min(1.0, (1 - r) / 0.5)) * (0.4 * np.pi)) / np.sin(0.4 * np.pi)))

def compute_score_weight(winning_score: int, losing_score: int):
    """Computes the score weight based on winning and total score."""
    total_score = winning_score + losing_score
    if winning_score >= 13 or total_score >= 19:
        return 1.0
    return min(1.0, np.sqrt((winning_score + max(losing_score, np.floor((winning_score - 1) / 2.0))) / (19.0)))

def compute_date_weight(week: int, total_weeks=14):
    """Computes the date weight based on how recent the game was played."""
    return 0.5 * (2 ** ((week - 1) / (total_weeks - 1)))

def is_ignorable_game(winner_rating, loser_rating, winning_score, losing_score, winner_games_played, threshold=5):
    """Check if the game should be ignored based on rating gap and score blowout."""
    if winner_rating - loser_rating > 600 and winning_score > (2 * losing_score + 1):
        return winner_games_played > threshold
    return False

def compute_team_rating(games, initial_rating=1000, iterations=1000):
    """Main iterative Elo-style rating algorithm."""
    team_ratings = {team: initial_rating for team in set(g['team'] for g in games)}
    total_weeks = max(g['week'] for g in games)

    for _ in range(iterations):
        new_ratings = {}

        for team in team_ratings:
            team_games = [g for g in games if g['team'] == team]
            eligible_games = 0
            game_ratings = []
            weight_sum = 0

            for game in team_games:
                opponent = game['opponent']
                opponent_rating = team_ratings.get(opponent, initial_rating)
                win = game['win']
                ws = game['winning_score']
                ls = game['losing_score']
                week = game['week']

                # Check if game should be ignored
                if win:
                    ignorable = is_ignorable_game(team_ratings[team], opponent_rating, ws, ls, eligible_games)
                else:
                    ignorable = is_ignorable_game(opponent_rating, team_ratings[team], ws, ls, eligible_games)

                if ignorable:
                    continue

                game_rating = calculate_game_rating(opponent_rating, win, ws, ls)
                score_weight = compute_score_weight(ws, ls)
                date_weight = compute_date_weight(week, total_weeks)
                weight = score_weight * date_weight

                game_ratings.append(game_rating * weight)
                weight_sum += weight
                eligible_games += 1

            new_ratings[team] = sum(game_ratings) / weight_sum if weight_sum > 0 else team_ratings[team]

        team_ratings = new_ratings

    return team_ratings

def populate_games():
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']
    documents = list(collection.find({}, {"_id": 0}))

    start_date = datetime.strptime("1/1/2025", "%m/%d/%Y")
    end_date = datetime.strptime("4/30/2025", "%m/%d/%Y")
    filtered_docs = []
    for doc in documents:
        doc_date = datetime.strptime(doc["event_date"], "%m/%d/%Y")
        if start_date <= doc_date <= end_date:
            filtered_docs.append(doc)

    games = []
    for document in filtered_docs:
        if int(document['home_score']) > int(document['away_score']):
            win = True
            winning_score = int(document['home_score'])
            losing_score = int(document['away_score'])
        else:
            win = False
            winning_score = int(document['away_score'])
            losing_score = int(document['home_score'])

        week = get_week(document['event_date'])

        game = {
            'team' : document['home_team'],
            'opponent' : document['away_team'],
            'win' : win,
            'winning_score' : winning_score,
            'losing_score' : losing_score,
            'week' : week
        }
        inverse = {
            'team' : document['away_team'],
            'opponent' : document['home_team'],
            'win' : not win,
            'winning_score' : winning_score,
            'losing_score' : losing_score,
            'week' : week
        }
        games.append(game)
        games.append(inverse)

    return games

def get_week(week: str):
    target_date = datetime.strptime(week, "%m/%d/%Y")
    start_date = datetime.strptime("1/1/2025", "%m/%d/%Y")

    delta_days = (target_date - start_date).days
    week_number = delta_days // 7 + 1

    return week_number

def get_top_20(team_ratings):
    team_ratings = sorted(team_ratings.items(), key=lambda item: item[1])

    top20 = []

    for i in range(20):
        top20.append(team_ratings[-(i+1)][0])

    return top20