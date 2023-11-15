import logging
from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL

from ExternalDatabaseEntry import ExternalDatabaseEntry
from ProteinScoringWeights.AFDBScores import *

logger = logging.getLogger(__name__)

class AFDBEntry(ExternalDatabaseEntry):

    def fetch(self) -> bytes:
        """ Fetch a .pdb file from AFDB database and return in string format. """
        # """Sends html request for all alphafold pdb file with the given id."""

        alphafold_id = "AF-" + self.entry_data["id"] + "-F1"
        database_version = "v4"
        model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{database_version}.pdb"
        try:
            f = urlopen(model_url)
            if f.getcode() == 200:
                return f.read()
            else:
                raise HTTPError(model_url, 404, "File not found")
        except Exception as e:
            raise Exception(e)

    def calculate_quality_score(self) -> float:
        """ Calculate quality score for this entry """
        logger.warning("AFDB Quality Score calculation not implemented: returning perfect score (1.0).")
        return 1.0