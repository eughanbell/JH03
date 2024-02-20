from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import PlainTextResponse, RedirectResponse
from typing import Annotated
import logging
from .database_entries import afdb_entry
from .pss import get_pdb_file, get_pdb_file_by_sequence, get_pdb_file_by_db_id, get_db_id_by_uniprot_id, upload_pdb_file
from .uniprot import ALPHAFOLD_DB_NAME

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastAPI()
HOST = "0.0.0.0"
PORT = 5000

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.exception_handler(404)
def handle_404():
    return redirect_to_docs()

@app.get("/retrieve_by_uniprot_id/{id}", response_class=PlainTextResponse)
def retrieve_by_uniprot_id(id: str, alphafold_only: bool = False, override_cache: bool = False,
                           db: Annotated[list[str] | None, Query()] = None):
    """Retrieves pdb file given the uniprot id for that protein structure.
    Tries to retrieve from cache first; If not present, finds the highest scoring file
    from uniprot and adds it to the cache before returning it.
    If the optional parameter alphafold_only == True then returns
    only the alphafold predicted entry"""
    if alphafold_only:
        return get_pdb_file(id, override_cache, use_dbs=[ALPHAFOLD_DB_NAME])
    else:
        return get_pdb_file(id, override_cache, use_dbs=db)


@app.get("/retrieve_by_sequence/{seq}", response_class=PlainTextResponse)
def retrieve_by_sequence(seq: str):
    """Retrieves pdb file given a part of the sequence for a protein structure.
    Pulls only from cache"""
    return get_pdb_file_by_sequence(seq)


@app.get("/retrieve_by_key/{key}", response_class=PlainTextResponse)
def retrieve_by_key(key: str):
    """Retrieves pdb file from cache using its unique key in the cache."""
    return get_pdb_file_by_db_id(key)


@app.get("/retrieve_key_by_uniprot_id/{id}", response_class=PlainTextResponse)
def retrieve_key_by_uniprot_id(id: str):
    """Retrieve unique cache key using the uniprot id for a protein structure."""
    return get_db_id_by_uniprot_id(id)


@app.post("/upload_pdb/", response_class=PlainTextResponse)
async def upload_pdb(file: UploadFile, id: str = "", db: str = "User Upload",
                     sequence: str = "", score: float = 0):
    """Allows user to upload a pdb file into the cache"""
    return upload_pdb_file(file.file.read().decode('utf-8'), db, id, sequence, score)
