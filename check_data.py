from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["harassment_db"]
collection = db["tweets"]

print("Total tweets :", collection.count_documents({}))

for tweet in collection.find({}, {"_id": 0}).limit(5):
    print(tweet)
