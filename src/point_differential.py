# chatgpt generated, tweaked by Kenji Her

from dotenv import load_dotenv
from pymongo import MongoClient
import os

def point_differential():
    # Connect to MongoDB
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']

    # Initialize team data
    team_stats = {}

    # Fetch all games from the collection
    games = collection.find()

    # Process each game
    for game in games:
        home_team, away_team = game["home_team"], game["away_team"]
        home_score, away_score = int(game["home_score"]), int(game["away_score"])
        
        point_diff_home = home_score - away_score
        point_diff_away = away_score - home_score

        # Update stats for home team
        if home_team not in team_stats:
            team_stats[home_team] = {"total_point_diff": 0, "average_point_diff": 0, "games_played": 0}
        team_stats[home_team]["total_point_diff"] += point_diff_home
        team_stats[home_team]["games_played"] += 1

        # Update stats for away team
        if away_team not in team_stats:
            team_stats[away_team] = {"total_point_diff": 0, "average_point_diff": 0, "games_played": 0}
        team_stats[away_team]["total_point_diff"] += point_diff_away
        team_stats[away_team]["games_played"] += 1

    # Compute and print the average point differential
    for team, stats in team_stats.items():
        if stats["games_played"] > 0:
            avg_point_diff = stats["total_point_diff"] / stats["games_played"]
        else:
            avg_point_diff = 0  # If a team has no games, avoid division by zero
        team_stats[team]["average_point_diff"] = float(f"{avg_point_diff:.2f}")

    return team_stats

def point_differential_against_top_teams(top_teams):
    # Connect to MongoDB
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']

    # Initialize team data
    team_stats = {}

    # Fetch all games from the collection
    games = collection.find()

    # Process each game
    for game in games:
        home_team, away_team = game["home_team"], game["away_team"]
        home_score, away_score = int(game["home_score"]), int(game["away_score"])

        point_diff_home = home_score - away_score
        point_diff_away = away_score - home_score

        # Only consider games against top teams
        if away_team in top_teams:
            if home_team not in team_stats:
                team_stats[home_team] = {"total_point_diff": 0, "games_played": 0}
            team_stats[home_team]["total_point_diff"] += point_diff_home
            team_stats[home_team]["games_played"] += 1

        if home_team in top_teams:
            if away_team not in team_stats:
                team_stats[away_team] = {"total_point_diff": 0, "games_played": 0}
            team_stats[away_team]["total_point_diff"] += point_diff_away
            team_stats[away_team]["games_played"] += 1

    # Compute and return the average point differential
    for team, stats in team_stats.items():
        if stats["games_played"] > 0:
            avg_point_diff = stats["total_point_diff"] / stats["games_played"]
        else:
            avg_point_diff = 0
        team_stats[team]["average_point_diff"] = float(f"{avg_point_diff:.2f}")

    return team_stats
