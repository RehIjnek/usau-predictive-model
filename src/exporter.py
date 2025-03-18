from dotenv import load_dotenv
from pymongo import MongoClient
import os

def export_data(home_teams, away_teams, home_scores, away_scores):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']
    
    documents = []
    for i in range(len(home_teams)):
        document = {
            'home_team' : home_teams[i],
            'away_team' : away_teams[i],
            'home_score' : home_scores[i],
            'away_score' : away_scores[i]
        }
        documents.append(document)
    collection.insert_many(documents, ordered=True)