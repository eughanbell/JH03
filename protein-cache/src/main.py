from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000


def get_file(uniprot_id):
    "Return pdb file data as a string,"
    "Or None if file is not in cache"
    # for testing on one specific id, as no cache exists right now
    if uniprot_id.lower() == "p02070":
        return "Foo protein 786ad87yasdy1d8h2o8uh238u83"
    return None


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    pdb_file = get_file(id)
    if pdb_file is not None:
        return {"present": True, "pdb_file": pdb_file}
    else:
        return {"present": False, "pdb_file": ""}


class ProteinFile(BaseModel):
    "Structure of json object to POST to store functions"
    uniprot_id: str
    pdb_file: str


@app.post("/protein_file/")
def store_by_uniprot_id(protein_file: ProteinFile):
    print(f"storing protein file: id:{protein_file.uniprot_id}"
          + " file:{protein_file.pdb_file}")
    return protein_file


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
