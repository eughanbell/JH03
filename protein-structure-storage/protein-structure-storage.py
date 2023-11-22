from src.main import uvicorn, app, HOST, PORT

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
