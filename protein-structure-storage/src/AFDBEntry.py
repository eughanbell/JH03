import logging
from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL

from .ExternalDatabaseEntry import ExternalDatabaseEntry
from .ProteinScoringWeights.AFDBWeights import *
from .helpers import get_from_url

logger = logging.getLogger(__name__)

class AFDBEntry(ExternalDatabaseEntry):

    master_weight = MASTER_WEIGHT

    def fetch(self) -> bytes:
        """ Fetch a .pdb file from AFDB database and return in string format. """
        # """Sends html request for all alphafold pdb file with the given id."""

        alphafold_id = "AF-" + self.entry_data["id"] + "-F1"
        database_version = "v4"
        model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{database_version}.pdb"
        return get_from_url(model_url)

    def calculate_raw_quality_score(self) -> float:
        """ Calculate quality score for this entry """
        logger.warning("AFDB Quality Score calculation not implemented: returning worst score (0.0).")
        return 0.0