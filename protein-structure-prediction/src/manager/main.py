from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse
from .CalculationManager import CalculationManager
from typing import Annotated
import logging

logger = logging.getLogger(__name__)
app = FastAPI()
HOST = "0.0.0.0"
PORT = 7000

@app.get("/list_calculations/", response_class=PlainTextResponse)
def list_calculations():
    """ Returns a list of all sequences which have been or are being processed,
     elapsed processing time and completion status.  """
    print("There are no ongoing calculations, returning empty list.")
    return CalculationManager.list_calculations()

@app.get("/calculate_protein_structure_from_sequence/{sequence}", response_class=PlainTextResponse)
def calculate_protein_structure_from_sequence(sequence: str):
    """ Enqueue another protein sequence to have its structure predicted.  """
    return CalculationManager.add_calculation(sequence)

@app.get("/download_structure/{sequence}", response_class=PlainTextResponse)
def download_structure(sequence: str):
    """ Download the structure of a sequence whose structure has been
     predicted, will return nothing if prediction not yet complete. """
    return CalculationManager.download_calculation_result(search_sequence = sequence)