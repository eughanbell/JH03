import logging
from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL

from .abstract_entry import ExternalDatabaseEntry
from .weight_importer import import_weights
from ..helpers import get_from_url

logger = logging.getLogger(__name__)

afdb_weights = {"final_score_multiplier": 0}
afdb_weights = import_weights(afdb_weights, "/src/config/afdb-weights.yaml")

class AFDBEntry(ExternalDatabaseEntry):

    def fetch(self) -> bytes:
        """ Fetch a .pdb file from AFDB database and return in string format. """
        # """Sends html request for all alphafold pdb file with the given id."""
        alphafold_id = "AF-" + self.entry_data["id"] + "-F1"
        database_version = "v4"
        model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{database_version}.pdb"
        return get_from_url(model_url).decode()

    def calculate_raw_quality_score(self) -> float:
        """ Calculate quality score for this entry """
        return afdb_weights["final_score_multiplier"]
