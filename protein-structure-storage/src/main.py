from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from . import AFDBEntry
from .pss import get_pdb_file, get_pdb_file_by_sequence, get_pdb_file_by_db_id

app = FastAPI()

HOST = "0.0.0.0"
PORT = 5000


@app.get("/retrieve_by_uniprot_id/{id}", response_class=PlainTextResponse)
def retrieve_by_uniprot_id(id: str, alphafold_only: bool = False):
    """If optional parameter alphafold_only == True then returns
    only the alphafold predicted entry"""
    if alphafold_only:
        try:
            request = AFDBEntry.AFDBEntry({"id": id.upper()})
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
