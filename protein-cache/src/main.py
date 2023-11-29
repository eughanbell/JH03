from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from db import get_cache, store_cache, get_by_sequence

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000


def pdb_response(pdb_file):
    if pdb_file is None:
        return {"present": False, "pdb_file": ""}
    return {"present": True, "pdb_file": pdb_file}


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    return pdb_response(get_cache(id))


@app.get("/retrieve_by_sequence/{sequence}")
def retrieve_by_sequence(sequence: str):
    return pdb_response(get_by_sequence(sequence))


class ProteinFile(BaseModel):
    "Structure of json object to POST to store functions"
    uniprot_id: str
    pdb_file: str
    sequence: str


@app.post("/protein_file/")
def store_protein_in_cache(protein_file: ProteinFile):
    print(f"storing protein file: id:{protein_file.uniprot_id}"
          + " file:{protein_file.pdb_file}")
    store_cache(protein_file.uniprot_id,
                protein_file.pdb_file,
                protein_file.sequence)
    return protein_file


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
