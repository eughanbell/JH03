import logging
from math import log, e
import re

from .abstract_entry import ExternalDatabaseEntry
from ..helpers import get_from_url
from .weight_importer import import_weights

logger = logging.getLogger(__name__)

pdbe_weights = {
    "final_score_multiplier": 1,
    "chain_length_multiplier": 1,
    "method_score_multiplier": 1,
    "resolution_multipler": 0.02,
    "default_chain_length_score": 0.1,
    "method_multiplier": {"default": 0.1},
    "resolution": {"interpolation": "exponential",
                   "weight_at_0": 1,
                   "weight_at_1": 0.9,
                   "default": 0.1},
}
pdbe_weights = import_weights(pdbe_weights, "/src/config/pdbe-weights.yaml")


class PDBeEntry(ExternalDatabaseEntry):

    def fetch(self) -> bytes:
        """ Fetch a .pdb file from PDBe database and return in string format. """
        pdb_id = self.extract_id()
        pdb_file = get_from_url(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_id}.ent")
        return pdb_file.decode()
        
    def calculate_raw_quality_score(self) -> float:
        """ Calculate unweighted quality score for this entry """
        
        # Load in uniprot metadata about this entry
        resolution = self.extract_resolution()
        method = self.extract_method()
        file_chain_length = self.extract_chain_length()
        full_chain_length = self.extract_full_chain_length()
        
        # Calculate individual scores for each category, based on protein metadata
        resolution_scores = [
            pdbe_weights["resolution_multipler"] * self.calculate_resolution_score(resolution),
            pdbe_weights["method_score_multiplier"] *  self.calculate_method_score(method),
            pdbe_weights["chain_length_multiplier"] * self.calculate_chain_length_score(file_chain_length, full_chain_length)
        ]
        # All resolution scores will be valid values (or defaults)

        # Weight and combine all scores into a single quality score
        avg_score = sum(resolution_scores) / len(resolution_scores)
        return pdbe_weights["final_score_multiplier"] * avg_score

    def extract_id(self) -> str:
        id = self.entry_data.get("id", "") #Will be empty string if id metadata unavailable
        if not id:
            logger.warning(f"Failed to determine id: could not determine data id from Uniprot metadata. Found method data of invalid format '{id}'")
            return None
        
        return id.lower()

    def extract_resolution(self) -> float:
        """ Extract resolution in Angstroms from resolution self.entry_data  """

        resolution_string = self.entry_data.get("resolution","") # Will be empty string if resolution metadata unavailable

        resolution_float_string = re.findall(r"^(\d+(?:\.?\d+)?) A$", resolution_string) # Captures decimal floats or ints in Angstroms
        if not resolution_float_string:
            # Received corrupt or unusually formatted metadata.
            logger.warning(f"PDBe: Failed to calculate resolution score: could not determine resolution from Uniprot metadata. Found resolution of invalid format '{resolution_string}' (expected '[integer] A' or '[float] A). Returning a resolution score of 0")
            return pdbe_weights["resolution"]["default"]
        
        resolution = float(resolution_float_string[0]) # This line is safe because regex always extracts a string which can yield either an integer or float
        return resolution

    def extract_chain_length(self) -> int:
        """ Extract the length of chain from chains self.entry_data """

        chains_string = self.entry_data.get("chains", "") # Will be empty string if chains metadata unavailable
        chain_ends = re.findall(r"[A-Z](?:/[A-Z]])?=(\d+)-(\d+)", chains_string) # Captures the beginning and end positions of the chain parts (there could be more than one, e.g. "A/B=1-23, C/D=47-94")
        chain_length = 0 # Cumulative chain length of all parts
        for chain_part_ends in chain_ends:
            chain_part_length = abs(int(chain_part_ends[1]) - int(chain_part_ends[0])) + 1 # 1 is added as chain end positions are both included in the chain
            chain_length += chain_part_length
        
        if chain_length > 0:
            return chain_length
        else:
            logger.warning(f"Failed to calculate chain length: could not determine chain length from Uniprot metadata. Found chains data of invalid format '{chains_string}'")
            return pdbe_weights["default_chain_length_score"]
    
    def extract_method(self) -> str:
        """ Extract the method of data acquisition from chains self.entry_data """
        method = self.entry_data.get("method", "")
        if not method:
            logger.warning(f"Failed to determine method score: could not determine data acquisition method from Uniprot metadata. Found method data of invalid format '{method}'")
            return None
        return method

    def extract_full_chain_length(self) -> int:
        """ Extract the chain length of the full protein from protein metadata """
        protein_metadata = self.entry_data.get("protein_metadata",{})
        sequence = protein_metadata.get("sequence","")
        reported_chain_length = 0
        string_chain_length = len(sequence)
        
        try:
            reported_chain_length = int(protein_metadata.get("sequence_length", 0))
        except ValueError:
            reported_chain_length = 0

        if reported_chain_length != string_chain_length:
            logger.warning(f"Protein chain length doesn't match reported chain length: attempting to select largest one. Reported chain length: '{reported_chain_length}', actual sequence: '{sequence}'.")
            full_chain_length = max(reported_chain_length, string_chain_length)
            if full_chain_length <= 0:
                logger.warning(f"Failed to reconcile protein chain lengths.")
                return 0
            else:
                return full_chain_length
        else:
            return reported_chain_length

    def calculate_resolution_score(self, resolution) -> float:
        """ Calculate score for this entry based on imaging resolution 
        
        Determines a weight to assign the entry, based on its image resolution in
        Angstroms. Infinite resolution (resolution value of 0 A) would receive
        a perfect weight of 1.

        If calculation cannot be performed, return default score.
        """

        if resolution == None:
            return pdbe_weights["resolution"]["default"] # Resolution score will be invalid if there is no resolution (thus resolution will be ignored in scoring)
        
        a = pdbe_weights["resolution"]["weight_at_1"] # The weight assigned to a resolution of 1, e.g., the point (1,a)
        if pdbe_weights["resolution"]["interpolation"] == "linear":
            gradient = (a-1) / 1.0
            return max((resolution * gradient) + 1, 0) # y = m*x + y-intercept
        elif pdbe_weights["resolution"]["interpolation"] == "exponential":
            decay_rate = log(a)
            return e**(decay_rate * resolution)
        else:
            logger.error(f"Failed to calculate resolution score: weights table specifies invalid interpolation scheme \"{pdbe_weights['resolution']['interpolation']}\" for resolution.")
            return pdbe_weights["resolution"]["default"]
    
    def calculate_method_score(self, method) -> float:
        """ Determine score based on acquisition method
         If calculation cannot be performed, return default score. """
        return pdbe_weights["method_multiplier"].get(
            method.lower(),
            pdbe_weights["method_multiplier"]["default"])
    
    def calculate_chain_length_score(self, file_chain_length, full_protein_chain_length) -> float:
        """ Calculate ratio of file chain length to full protein chain length

         If calculation cannot be performed, return default score. """

        if file_chain_length == None or full_protein_chain_length == None or full_protein_chain_length == 0:
            # If the whole protein length is 0, data is likely corrupted and the fraction that file_chain_length represents cannot be meaningfully extracted, so return default
            return pdbe_weights["default_chain_length_score"] # Missing data, return default
        
        return abs(file_chain_length) / abs(full_protein_chain_length) # Convert to absolute value to handle accidental negation of input data
