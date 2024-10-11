from flask import Flask
import redis
import pymongo
import os

app = Flask(__name__)

# Initialize Redis
r = redis.Redis(host="redis", port=6379)

# Initialize MongoDB connection
def get_mongo_connection():
    client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    db = client.flask_db  # Database initialized in docker-compose
    return db

@app.route("/")
def home():
    # Redis hit counter
    count = r.incr("hits")
    
    # MongoDB interaction: Insert visit record
    db = get_mongo_connection()
    visits_collection = db.visits
    visit = {"visit_number": count}
    visits_collection.insert_one(visit)
    
    # Count the number of visits stored in MongoDB
    mongo_count = visits_collection.count_documents({})
    
    return f"This page has been visited {count} times (Redis). {mongo_count} visits have been recorded in MongoDB."


if __name__ == "__main__":
    app.run(host="0.0.0.0")
