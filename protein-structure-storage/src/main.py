from urllib.error import HTTPError
from fastapi import FastAPI, HTTPException
import uvicorn
from . import AFDBEntry
from .pss import get_pdb_file, get_pdb_file_by_sequence

app = FastAPI()

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str, alphafold_only: bool = False):
    """If optional parameter alphafold_only == True then returns
    only the alphafold predicted entry"""
    if alphafold_only:
        try:
            request = AFDBEntry.AlphaFoldRequest(id)
            return {"pdb": request.request_pdb()}
        except HTTPError as e:
            return {"Error": "404: page not found check you have entered the URL correctly"}
        except Exception as e:
            return {"Error": e.args[0]}
    else:
        return {"pdb_file": get_pdb_file(id)}


@app.get("/retrieve_by_sequence/{seq}")
def retrieve_by_sequence(seq: str):
    return {"pdbfile": get_pdb_file_by_sequence(seq)}


@app.get("/retrieve_by_key/{key}")
def retrieve_by_key(key: int):
    return {"key": key}
