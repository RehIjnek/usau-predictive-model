from dotenv import load_dotenv
from pymongo import MongoClient
import os

def export_games(event_name, event_date, home_teams, away_teams, home_scores, away_scores):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['games']
    
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

def export_wl(team_records):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['records']

    documents = []
    for team, record in team_records.items():
        document = {
            'team_name' : team,
            'wins' : record['wins'],
            'losses' : record['losses']
        }
        documents.append(document)
    if documents:
        collection.insert_many(documents, ordered=True)

def export_pd(team_stats):
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['usau']
    collection = db['stats']

    documents = []
    for team, stats in team_stats.items():
        document = {
            'team_name' : team,
            'tpd' : stats['total_point_diff'],
            'apd' : stats['average_point_diff'],
            'games_played' : stats['games_played']
        }
        documents.append(document)
    if documents:
        collection.insert_many(documents, ordered=True)
