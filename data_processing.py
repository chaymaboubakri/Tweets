# data_processing.py

import pandas as pd
import re
import uuid
from datetime import datetime
from pymongo import MongoClient

# 1. Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["harassment_db"]
collection = db["tweets"]

# 2. Fonction de nettoyage du texte
def clean_tweet(text):
    text = text.lower()                              # minuscules
    text = re.sub(r'@\w+', '', text)                 # supprimer mentions
    text = re.sub(r'http\S+', '', text)              # supprimer URLs
    text = re.sub(r'[^\w\s]', '', text)              # ponctuation
    text = re.sub(r'\s+', ' ', text).strip()         # espaces inutiles
    return text

def main():
    # 3. Lecture du CSV
    df = pd.read_csv("data/cyberbullying_tweets.csv")

    # 4. Suppression des doublons
    df = df.drop_duplicates(subset=["tweet_text"])

    # 5. Nettoyage
    df["cleaned_tweet_text"] = df["tweet_text"].apply(clean_tweet)

    # 6. Longueur du tweet nettoyé
    df["tweet_length"] = df["cleaned_tweet_text"].apply(len)

    # 7. Génération ID + date ingestion
    df["tweet_id"] = [str(uuid.uuid4()) for _ in range(len(df))]
    df["ingestion_date"] = datetime.utcnow()

    # 8. Sélection des colonnes utiles
    final_df = df[[
        "tweet_id",
        "cleaned_tweet_text",
        "cyberbullying_type",
        "tweet_length",
        "ingestion_date"
    ]]

    # 9. Insertion MongoDB
    collection.insert_many(final_df.to_dict("records"))

    print("Données nettoyées et insérées avec succès.")

if __name__ == "__main__":
    main()
