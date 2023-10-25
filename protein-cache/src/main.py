from fastapi import FastAPI
import uvicorn

app = FastAPI()
HOST = "0.0.0.0"
PORT = 6000

@app.get("/contains_uniprot_id/{id}")
def contains_uniprot_id(id: str):
    return {"id": id, "present": False}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
