from pymongo import MongoClient
from bson import ObjectId
import time

def wait_for_mongo(host="mongo:27017", retries=5, delay=5):

    # Create a temporary client with a short serverSelectionTimeout
    temp_client = MongoClient(host=host, serverSelectionTimeoutMS=1000)  # Short timeout for initial connection attempts
    for attempt in range(retries):
        try:
            # Attempt to ping the MongoDB server
            temp_client.admin.command('ping')
            print("MongoDB is ready!")
            return True  # MongoDB is ready
        except Exception as e:
            print(f"Waiting for MongoDB... Attempt {attempt + 1}/{retries}")
            time.sleep(delay)
    raise Exception("MongoDB not ready after max retries. Exiting.")

# Wait for MongoDB to be ready before establishing a permanent connection
wait_for_mongo()

# Connect to running database with a longer timeout now that we know MongoDB is ready
client = MongoClient(host="mongo:27017", serverSelectionTimeoutMS=30000)

# Deletes database - for development
client.drop_database("cache")

# Get an object representing the cache db
db = client["cache"]


def get_cache(uniprot_id, field="pdb_file"):
    "return pdb file if in cache"
    "otherwise returns None"
    e = db.cache.find_one({"uniprot_id": uniprot_id.upper()})
    if e is None:
        return None
    return e.get(field)


def get_by_sequence(sequence, field="pdb_file"):
    e = db.cache.find_one({"sequence": {"$regex": sequence.upper()}})
    if e is None:
        return None
    return e.get(field)


def get_by_db_id(obj_id, field="pdb_file"):
    try:
        e = db.cache.find_one({"_id": ObjectId(obj_id)})
        if e is None:
            return None
        return e.get(field)
    except Exception:
        return None


def store_cache(uniprot_id, pdb_file, sequence, source_db):
    "stores the given id and file in the cache"
    if uniprot_id == "" or get_cache(uniprot_id) is None:
        result = db.cache.insert_one({"uniprot_id": uniprot_id.upper(),
                                      "pdb_file": pdb_file,
                                      "sequence": sequence.upper(),
                                      "source_db": source_db})
        return str(result.inserted_id)
    else:
        print("WARNING: tried to store pdb file into database"
              + " That already contains an element with the same"
              + " uniprot id")
        return ""
