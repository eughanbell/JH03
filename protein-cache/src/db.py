from pymongo import MongoClient
import time
from hashlib import blake2b

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

db = client["cache"]

def get_cache(search_dict, source_dbs=None, field="pdb_file"):
    """Return field if in cache, otherwise returns None.
       source_dbs is list of pdb dbs to search (use all by default).
       If there are multiple matching entries, return the heighest scoring.
    """
    if isinstance(source_dbs, list):
        source_dbs = [x.upper() for x in source_dbs]
        search_dict["source_db"] = {"$in":source_dbs};
    e = db.cache.find(search_dict)
    if e is None:
        return None
    e = e.sort({"score": -1}).limit(1)
    try:
        return e.next().get(field)
    except Exception:
        return None


def store_cache(uniprot_id, pdb_file, sequence, source_db, score):
    """stores the given id and file in the cache.

    If uniprot id is blank, the file will always be added.
    If the uniprot id is already present, then:
     - if the source_db is new the file is added
     - if there is already an entry from that source_db
       it will be replaced if the pdb_file is different
    """
    pdb_hash = blake2b(pdb_file.encode()).hexdigest()
    uniprot_id = uniprot_id.upper()
    source_db = source_db.upper()
    obj_info = {"uniprot_id": uniprot_id,
                "source_db": source_db,
                "score": score,
                "sequence": sequence.upper(),
                "pdb_file": pdb_file,
                "hash": pdb_hash,}
    e = None
    if uniprot_id != "":
        e = db.cache.find_one(
            {"uniprot_id": uniprot_id, "source_db": source_db})
        if e is not None and e.get("hash") != pdb_hash:
            print("Updated existing entry")
            result = db.cache.replace_one(e, obj_info)
            return str(e.get("_id"))
    if e is None:
        print("Inserted into cache")
        result = db.cache.insert_one(obj_info)
        return str(result.inserted_id)
    print("Already in cache")
    return ""


def clear_cache():
    client.drop_database("cache")
