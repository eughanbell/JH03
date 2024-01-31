from src.main import app, HOST, PORT
import uvicorn
import subprocess

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
