from dotenv import load_dotenv
from pymongo import MongoClient
import os

def export_games(event_name, event_date, home_teams, away_teams, home_scores, away_scores):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games2']
    
    documents = []
    for i in range(len(home_teams)):
        document = {
            'event_name' : event_name,
            'event_date' : event_date,
            'home_team' : home_teams[i],
            'away_team' : away_teams[i],
            'home_score' : home_scores[i],
            'away_score' : away_scores[i]
        }
        documents.append(document)
    if documents:
        collection.insert_many(documents, ordered=True)