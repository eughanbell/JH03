import logging
from math import log, e
import re

from ExternalDatabaseEntry import ExternalDatabaseEntry
from ProteinScoringWeights.PDBeScores import *
from helpers import get_from_url

print(RELATIVE_WEIGHTS)

logger = logging.getLogger(__name__)

# {'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145'}

class PDBeEntry(ExternalDatabaseEntry):

    def fetch(self) -> bytes:
        """ Fetch a .pdb file from PDBe database and return in string format. """
        raise NotImplementedError("PDBe fetch not implemented.")

    def calculate_quality_score(self):
        """ Fetch or calculate quality score for this entry """
        
        # Load in uniprot metadata about this entry
        resolution = self.extract_resolution()
        method = self.extract_method()
        file_chain_length = self.extract_chain_length()
        full_protein_chain_length = 500
        logger.warning(f"NotImplemented: finding full protein length to compute coverage not yet implemented, assuming full length to be {full_protein_chain_length}.")

        # Calculate individual scores for each category, based on protein metadata
        resolution_score = self.calculate_resolution_score(resolution)
        method_score = self.calculate_method_score(method)
        chain_length_score = self.calculate_chain_length_score(file_chain_length, full_protein_chain_length)

        # Weight and combine all scores into a single quality score
        logger.warning("NotImplemented: calculating overall quality score not properly implemented. Will crash on invalid data.")
        self.quality_score = (RELATIVE_WEIGHTS["resolution"] * resolution_score +
                              RELATIVE_WEIGHTS["method"] *  method_score +
                              RELATIVE_WEIGHTS["chain_length"] * chain_length_score)/(sum(RELATIVE_WEIGHTS.values()))

    def extract_resolution(self) -> float:
        """ Extract resolution in Angstroms from resolution self.entry_data  """

        resolution_string = self.entry_data.get("resolution","") # Will be empty string if resolution metadata unavailable

        resolution_float_string = re.findall(r"^(\d+(?:\.?\d+)?) A$", resolution_string) # Captures decimal floats or ints in Angstroms
        if not resolution_float_string:
            # Received corrupt or unusually formatted metadata.
            logger.warning(f"Failed to calculate resolution score: could not determine resolution from Uniprot metadata. Found resolution of invalid format '{resolution_string}' (expected '[integer] A' or '[float] A).")
            return None
        
        resolution = float(resolution_float_string[0]) # This line is safe because regex always extracts a string which can yield either an integer or float
        return resolution

    def extract_chain_length(self) -> int:
        """ Extract the length of chain from chains self.entry_data """

        chains_string = self.entry_data.get("chains", "") # Will be empty string if chains metadata unavailable
        chain_ends = re.findall(r"^[A-Z]/[A-Z]=(\d+)-(\d+)$", chains_string) # Captures the beginning and end positions of the chain
        if len(chain_ends) == 1 and len(chain_ends[0]) == 2:
            # If findall returns 1 match and that match includes both numbers
            chain_length = int(chain_ends[0][1]) - int(chain_ends[0][0]) + 1 # 1 is added as chain end positions are both included in the chain
            if chain_length >= 0:
                return chain_length
            else:
                logger.warning(f"Failed to calculate chain length: got negative chain length from Uniprot metadata. Found chains data of invalid format '{chains_string}'")
                return None
        else:
            logger.warning(f"Failed to calculate chain length: could not determine chain length from Uniprot metadata. Found chains data of invalid format '{chains_string}'")
            return None
    
    def extract_method(self) -> str:
        """ Extract the method of data acquisition from chains self.entry_data """
        method = self.entry_data.get("method", "")
        if not method:
            logger.warning(f"Failed to determine method score: could not determine data acquisition method from Uniprot metadata. Found method data of invalid format '{method}'")
            return None
        return method

    def calculate_resolution_score(self, resolution) -> float:
        """ Calculate score for this entry based on imaging resolution 
        
        Determines a weight to assign the entry, based on its image resolution in
        Angstroms. Infinite resolution (resolution value of 0 A) would receive
        a perfect weight of 1.
        """

        if resolution == None:
            return None # Resolution score will be invalid if there is no resolution (thus resolution will be ignored in scoring)
        
        a = RESOLUTION_WEIGHTS["weight_at_1"] # The weight assigned to a resolution of 1, e.g., the point (1,a)
        if RESOLUTION_WEIGHTS["interpolation"] == "linear":
            gradient = (1-a) / 1.0
            return max((resolution * gradient) + a, 0) # y = m*x + y-intercept
        elif RESOLUTION_WEIGHTS["interpolation"] == "exponential":
            decay_rate = log(a)
            return e**(decay_rate * resolution)
        else:
            logger.error(f"Failed to calculate resolution score: weights table specifies invalid interpolation scheme '{RESOLUTION_WEIGHTS['interpolation']}' for resolution.")
            return None
    
    def calculate_method_score(self, method) -> float:
        """ Determine score based on acquisition method """
        return METHOD_WEIGHTS.get(method, None)
    
    def calculate_chain_length_score(self, file_chain_length, full_protein_chain_length) -> float:
        """ Calculate ratio of file chain length to full protein chain length"""

        if file_chain_length == None or full_protein_chain_length == None:
            return None
        
        if file_chain_length <= 0 or full_protein_chain_length <= 0:
            return 0
        return file_chain_length / full_protein_chain_length
    
    def __lt__(self, other): # Sorting / comparision is based on quality score
        return self.get_quality_score() < other.get_quality_score()
    
    def __repr__(self):
        return f"{self.entry_data}: {self.get_quality_score()}"