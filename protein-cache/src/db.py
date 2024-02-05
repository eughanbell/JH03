from pymongo import MongoClient
from bson import ObjectId
from hashlib import blake2b

# connect to running database
client = MongoClient(host="mongo:27017", # the internal docker address
                     serverSelectionTimeoutMS=3000)

# deletes database - for development
client.drop_database("cache")

# get an object representing the cache db
# will be implicitly created upon first inserting
# some data into the db
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
    pdb_hash = blake2b(pdb_file.encode()).hexdigest()
    e = None
    if uniprot_id != "":
        e = db.cache.find_one({"uniprot_id": uniprot_id.upper(),
                               "hash": pdb_hash})
    if e is None:
        result = db.cache.insert_one({"uniprot_id": uniprot_id.upper(),
                                      "hash": pdb_hash,
                                      "pdb_file": pdb_file,
                                      "sequence": sequence.upper(),
                                      "source_db": source_db})
        return str(result.inserted_id)
    return ""
