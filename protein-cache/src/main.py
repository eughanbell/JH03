from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    return {"present": False}


class ProteinFile(BaseModel):
    "Structure of json object to POST to store functions"
    uniprot_id: str
    pdb_file: str


@app.post("/protein_file/")
def store_by_uniprot_id(protein_file: ProteinFile):
    print(f"id:{protein_file.uniprot_id} file:{protein_file.pdb_file}")
    return protein_file


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
