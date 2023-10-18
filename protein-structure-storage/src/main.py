from fastapi import FastAPI
import uvicorn


# prints Hello World!
print("Hello, World!")

app = FastAPI()

DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 5000


@app.get("/example_endpoint")
def example_endpoint():
    return {"Hello from this endpoint!\n"}


@app.get("/retrieve_by_uniprot_id/{id}")
def retrieve_by_uniprot_id(id: str):
    return {"You asked for id": id}


@app.get("/retrieve_by_sequence/{seq}")
def retrieve_by_sequence(seq: str):
    return {"You asked for seq": seq}


@app.get("/retrieve_by_key/{key}")
def retrieve_by_key(key: int):
    #print(f"got key: {key}")
    return {"You asked for key": key}


@app.exception_handler(404)
def unknown_url(error):
    return "Error: The requested endpoint does not exist!\n", 404

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    if not DEBUG_MODE:
        # use waitress for WSGI server in a production setting
        from waitress import serve
        serve(app, host=HOST, port=PORT)
    else:
        uvicorn.run(app ,host=HOST, port=PORT)
