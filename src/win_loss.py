# chatgpt generated, tweaked by Kenji Her

from dotenv import load_dotenv
from pymongo import MongoClient
import os

def win_loss():
    # Connect to MongoDB
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']

    # Initialize team records
    team_records = {}

    # Fetch all games from the collection
    games = collection.find()

    # Process each game
    for game in games:
        home_team, away_team = game["home_team"], game["away_team"]
        home_score, away_score = int(game["home_score"]), int(game["away_score"])

        # Initialize teams in dictionary if not present
        if home_team not in team_records:
            team_records[home_team] = {"wins": 0, "losses": 0}
        if away_team not in team_records:
            team_records[away_team] = {"wins": 0, "losses": 0}

        # Determine winner and update records
        if home_score > away_score:
            team_records[home_team]["wins"] += 1
            team_records[away_team]["losses"] += 1
        else:
            team_records[away_team]["wins"] += 1
            team_records[home_team]["losses"] += 1

    return team_records