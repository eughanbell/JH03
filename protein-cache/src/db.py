from pymongo import MongoClient
from bson import ObjectId
from hashlib import blake2b

# connect to running database
client = MongoClient(host="mongo:27017", # the internal docker address
                     serverSelectionTimeoutMS=3000)

# deletes database - for development
#client.drop_database("cache")

# get an object representing the cache db
# will be implicitly created upon first inserting
# some data into the db
db = client["cache"]


def get_cache(uniprot_id, field="pdb_file", source_dbs=None):
    """Return pdb file if in cache, otherwise returns None.
       Source_dbs is list of source_dbs to search (use all by default).
       If there are multiple matching entries, return the heighest scoring.
    """
    e = None
    if isinstance(source_dbs, list):
        source_dbs = [x.upper() for x in source_dbs]
        e = db.cache.find({"uniprot_id": uniprot_id.upper(),
                           "source_db":{"$in":source_dbs}})
    else:
        e = db.cache.find({"uniprot_id": uniprot_id.upper()})
    if e is None:
        return None
    e = e.sort({"score": -1}).limit(1)
    try:
        return e.next().get(field)
    except StopIteration:
        return None


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
