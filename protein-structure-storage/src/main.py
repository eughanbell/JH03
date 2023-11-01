from fastapi import FastAPI, HTTPException
import uvicorn
import alphaFoldDBrequest

app = FastAPI()

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str, alphafold_only: bool = False):
    """If optional parameter alphafold_only == True then returns only the alphafold predicted entry"""
    if alphafold_only:
        request = alphaFoldDBrequest.AlphaFoldRequest(id)
        return {"pdb": request.request_pdb()}
    else:
        return {"test": id}


@app.get("/retrieve_by_sequence/{seq}")
def retrieve_by_sequence(seq: str):
    return {"seq": seq}


@app.get("/retrieve_by_key/{key}")
def retrieve_by_key(key: int):
    return {"key": key}


if __name__ == "__main__":
    uvicorn.run(app ,host=HOST, port=PORT)
