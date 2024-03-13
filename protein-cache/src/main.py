from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import uvicorn
from pydantic import BaseModel
from db import store_cache, get_cache
from typing import Annotated
from bson import ObjectId

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000


def json_response(data, field="pdb_file"):
    if data is None or data == "None":
        return {"present": False, field: ""}
    return {"present": True, field: data}


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str, source_dbs: Annotated[list[str] | None, Query()] = None):
    return json_response(
        get_cache({"uniprot_id": id.upper()}, source_dbs))


@app.get("/retrieve_by_sequence/{sequence}")
def retrieve_by_sequence(sequence: str, source_dbs: Annotated[list[str] | None, Query()] = None):
    return json_response(
        get_cache({"sequence": {"$regex": sequence.upper()}}, source_dbs))


@app.get("/retrieve_by_db_id/{db_id}")
def retrieve_by_db_id(db_id: str):
    return json_response(
        get_cache({"_id": ObjectId(db_id)}))


@app.get("/retrieve_db_id_by_uniprot_id/{id}")
def retrieve_db_id_by_uniprot_id(id: str, source_dbs: Annotated[list[str] | None, Query()] = None):
    return json_response(
        str(get_cache({"uniprot_id": id.upper()}, field="_id", source_dbs=source_dbs)), field="db_id")


class ProteinFile(BaseModel):
    "Structure of json object to POST to store functions"
    uniprot_id: str
    pdb_file: str
    sequence: str
    source_db: str
    score: float


@app.post("/protein_file/", response_class=PlainTextResponse)
def store_protein_in_cache(protein_file: ProteinFile):
    print(f"storing protein file: id:{protein_file.uniprot_id}")
    return store_cache(protein_file.uniprot_id,
                protein_file.pdb_file,
                protein_file.sequence,
                protein_file.source_db,
                protein_file.score)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
