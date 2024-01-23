from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from db import get_cache, store_cache, get_by_sequence, get_by_db_id

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000


def json_response(data, field="pdb_file"):
    if data is None or data == "None":
        return {"present": False, field: ""}
    return {"present": True, field: data}


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    return json_response(get_cache(id))


@app.get("/retrieve_by_sequence/{sequence}")
def retrieve_by_sequence(sequence: str):
    return json_response(get_by_sequence(sequence))


@app.get("/retrieve_by_db_id/{db_id}")
def retrieve_by_db_id(db_id: str):
    return json_response(get_by_db_id(db_id))


@app.get("/retrieve_db_id_by_uniprot_id/{id}")
def retrieve_db_id_by_uniprot_id(id: str):
    return json_response(str(get_cache(id, field="_id")), field="db_id")


class ProteinFile(BaseModel):
    "Structure of json object to POST to store functions"
    uniprot_id: str
    pdb_file: str
    sequence: str
    source_db: str


@app.post("/protein_file/")
def store_protein_in_cache(protein_file: ProteinFile):
    print(f"storing protein file: id:{protein_file.uniprot_id}")
    store_cache(protein_file.uniprot_id,
                protein_file.pdb_file,
                protein_file.sequence,
                protein_file.source_db)
    return protein_file


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
