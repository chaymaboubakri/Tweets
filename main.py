# main.py

from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(title="Cyberbullying API")

client = MongoClient("mongodb://localhost:27017/")
db = client["harassment_db"]
collection = db["tweets"]

# 1. Endpoint racine
@app.get("/")
def root():
    return {"message": "Bienvenue dans l'API de détection de harcèlement !"}

# 2. Tweets paginés
@app.get("/tweets")
def get_tweets(skip: int = 0, limit: int = 10):
    tweets = list(
        collection.find({}, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )
    return tweets

# 3. Statistiques globales
@app.get("/stats")
def get_stats():
    total = collection.count_documents({})

    # Répartition par type
    pipeline = [
        {"$group": {"_id": "$cyberbullying_type", "count": {"$sum": 1}}}
    ]
    distribution = {doc["_id"]: doc["count"] for doc in collection.aggregate(pipeline)}

    # Longueur moyenne
    avg_length = list(collection.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$tweet_length"}}}
    ]))[0]["avg"]

    return {
        "total_tweets": total,
        "distribution": distribution,
        "average_tweet_length": round(avg_length, 2)
    }
