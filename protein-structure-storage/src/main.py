from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse
from typing import Annotated
import logging
from .database_entries import afdb_entry
from .pss import get_pdb_file, get_pdb_file_by_sequence, get_pdb_file_by_db_id, get_db_id_by_uniprot_id, upload_pdb_file

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastAPI()
HOST = "0.0.0.0"
PORT = 5000


@app.get("/retrieve_by_uniprot_id/{id}", response_class=PlainTextResponse)
def retrieve_by_uniprot_id(id: str, alphafold_only: bool = False):
    """If optional parameter alphafold_only == True then returns
    only the alphafold predicted entry"""
    if alphafold_only:
        try:
            request = afdb_entry.AFDBEntry({"id": id.upper()})
            return request.fetch()
        except Exception:
            return ""
    else:
        return get_pdb_file(id)


@app.get("/retrieve_by_sequence/{seq}", response_class=PlainTextResponse)
def retrieve_by_sequence(seq: str):
    return get_pdb_file_by_sequence(seq)


@app.get("/retrieve_by_key/{key}", response_class=PlainTextResponse)
def retrieve_by_key(key: str):
    return get_pdb_file_by_db_id(key)


@app.get("/retrieve_key_by_uniprot_id/{id}", response_class=PlainTextResponse)
def retrieve_key_by_uniprot_id(id: str):
    return get_db_id_by_uniprot_id(id)


@app.post("/upload_pdb/", response_class=PlainTextResponse)
async def upload_pdb(file: UploadFile):
    return upload_pdb_file(file.file.read().decode('utf-8'), "User Upload")
