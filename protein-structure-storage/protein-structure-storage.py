from src.main import app, HOST, PORT
from src.database_entries.afdb_entry import afdb_weights
from src.database_entries.pdbe_entry import pdbe_weights
import uvicorn
import subprocess
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"AFDB Weight Dict: {afdb_weights}")
    logger.info(f"PDBe Weight Dict: {pdbe_weights}")
    uvicorn.run(app, host=HOST, port=PORT)
