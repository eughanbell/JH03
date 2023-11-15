from pymongo import MongoClient

# connect to running database
client = MongoClient(host="mongo:27017", # the internal docker address
                     serverSelectionTimeoutMS=3000)

# deletes database - easier for testing
# remove at some point.
client.drop_database("cache")

# get an object representing the cache db
# will be implicitly created upon first inserting
# some data into the db
db = client["cache"]

# test entry
db.cache.insert_one({
    "uniprot_id": "P02070",
    "pdb_file": "I AM A PDB FILE IN A MONGODB DATABASE",
})


def get_cache(uniprot_id):
    "return pdb file if in cache"
    "otherwise returns None"
    e = db.cache.find_one({"uniprot_id": uniprot_id.upper()})
    if e is None:
        return None
    return e.get("pdb_file")


def store_cache(uniprot_id, pdb_file):
    "stores the given id and file in the cache"
    if get_cache(uniprot_id) is None:
        db.cache.insert_one({"uniprot_id": uniprot_id.upper(),
                             "pdb_file": pdb_file})
    else:
        print("WARNING: tried to store pdb file into database"
              + " That already contains an element with the same"
              + " uniprot id")
