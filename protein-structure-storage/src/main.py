from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    return {"uniprot_id": id}


@app.get("/retrieve_by_sequence/{seq}")
def retrieve_by_sequence(seq: str):
    return {"seq": seq}


@app.get("/retrieve_by_key/{key}")
def retrieve_by_key(key: int):
    return {"key": key}


if __name__ == "__main__":
    uvicorn.run(app ,host=HOST, port=PORT)
