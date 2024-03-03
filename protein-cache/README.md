# Protein Cache - Internal Architecture

  

The overall goal of this container is to efficiently retrieve and store protein structures and related data. It aims to reduce redundant fetch operations by cachine results from previous queries. This container interfaces with a MongoDB database to cache protein data, including sequences, structure files (PDB files), and metadata sourced from various databases.

The cache's main job is to return a cached protein file if one is available. It can also search through the cache, checking the cached protein's sequence against a sequence to search for.

---
**MongoDB**
MongoDB doesn't use tables ([unlike SQL databases](https://www.mongodb.com/docs/manual/reference/sql-comparison/)), instead data is stored in collections. 
Collections are lists of text documents in the BSON format (JSON-like).
So each entry in a collection is a text document. The primary key is automatically generated. 

This is what an entry in a collection looks like (where this is a file):
```BSON
{                                            
  _id: ObjectId("509a8fb2f3f4948bd2f983a0"), 
  user_id: "abc123",                         
  age: 55,                                   
  status: 'A'                                
}                                            
```
It's worth noting that different objects in a collection do not need to have the same fields.
[Source for most of this](https://www.mongodb.com/docs/manual/faq/fundamentals/)
[Here's a guide on using a mongodb database](https://www.mongodb.com/docs/manual/crud/#std-label-crud)

---
**How each Protein record is stored in the cache**

```
obj_info = {
	"uniprot_id":uniprot_id,
	"source_db": source_db,
	"score": score,
	"sequence": sequence.upper(),
	"pdb_file": pdb_file,
	"hash": pdb_hash,
	}
```

---
This service exposes the following endpoints for interacting with the cache.

**Retrieval Endpoints:**

 ```
 GET '/retrieve_by_uniprot_id/{id}'
 ```
- Retrieves a protein structure by UniProtID
- Optional query parameter 'source_dbs' to specify databases to search

```
GET /retrieve_by_sequence/{sequence}'
```
- Retrieves a protein structure by sequence

```
GET '/retrieve_by_db_id/{db_id}'
```
- Retrieves a protein structure by its MongoDB '_id'
 
```
GET '/retrieve_db_id_by_uniprot_id/{id}
```
- Retrieves the MongoDB '_id' of a caches entry using a UniProtID

**Storage Endpoint:**
```
POST '/protein_file/'
```
- Stores a new protein structure in the cache
- Accepts JSON payload with 'uniprot_id', 'pdb_file', 'sequence', 'source_db', and 'source'.

---


**Inspecting the Cache**

Ensure the containers are running, go to `127.0.0.1:8082` in your browser. You will need to login, the credentials are

```
username: admin
password: pass
```

The cache database will only be present if at least one pdb file has been requested.

---
