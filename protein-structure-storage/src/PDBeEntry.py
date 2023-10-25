import logging
from math import log, e
import re
from ExternalDatabaseEntry import ExternalDatabaseEntry

logger = logging.getLogger(__name__)

METHOD_WEIGHTS = {
    "X-ray": 1,   
}

RESOLUTION_WEIGHTS = {
    "interpolation": "exponential",
    # Weight at 0 is assumed to be 1 (infinite resolution scores 1)
    "weight_at_1": 0.9
}

# {'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145'}

class PDBeEntry(ExternalDatabaseEntry):

    def fetch(self) -> str:
        """ Fetch a .pdb file from PDBe database and return in string format. """
        raise NotImplementedError("PDBe fetch not implemented.")

    def calculate_quality_score(self):
        """ Fetch or calculate quality score for this entry """
        
        resolution = self.extract_resolution()
        method = self.extract_method()
        file_chain_length = self.extract_chain_length()
        full_protein_chain_length = 500 # This needs to be calculated
        logger.warning("NotImplemented: finding full protein length not yet implemented, assuming length to be 500.")

        resolution_score = self.calculate_resolution_score(resolution)
        method_score = self.calculate_method_score(method)
        chain_length_score = self.calculate_chain_length_score(file_chain_length, full_protein_chain_length)

        logger.warning("NotImplemented: calculating overall quality score not properly implemented. Will crash on invalid data.")
        self.quality_score = (resolution_score + method_score + chain_length_score)/3

    def extract_resolution(self) -> float:
        """ Extract resolution in Angstroms from resolution self.entry_data  """

        resolution_string = self.entry_data.get("resolution","")

        resolution_float_string = re.findall(r"^(\d+(?:\.?\d+)?) A$", resolution_string) # Captures decimal floats or ints in Angstroms
        if not resolution_float_string:
            logger.warning(f"Failed to calculate resolution score: entry_data resolution of invalid format '{resolution_string}'.")
            return None
        resolution = float(resolution_float_string[0])
        return resolution

    def extract_chain_length(self) -> int:
        """ Extract the length of chain from chains self.entry_data """

        chains_string = self.entry_data.get("chains", "")
        chain_ends = re.findall(r"^B/D=(\d+)\-(\d+)$", chains_string)
        if len(chain_ends) == 2:
            return int(chain_ends[1]) - int(chain_ends[0]) + 1 # Chain ends are assumed to be inclusive
        else:
            logger.warning(f"Failed to calculate chain length: chains data of invalid format '{chains_string}'")
            return None
    
    def extract_method(self) -> str:
        """ Extract the method of data acquisition from chains self.entry_data """
        method = self.entry_data.get("method", "")
        if not method:
            logger.warning(f"Failed to determine method score: entry_data method of invalid format '{method}'")
            return None
        return method

    def calculate_resolution_score(self, resolution) -> float:
        """ Calculate score for this entry based on imaging resolution 
        
        Determines a weight to assign the entry, based on its image resolution in
        Angstroms. Infinite resolution (resolution value of 0 A) would receive
        a perfect weight of 1.
        """

        if not resolution:
            return None

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
    
    def calculate_chain_length_score(file_chain_length, full_protein_chain_length) -> float:
        """ Calculate ratio of file chain length to full protein chain length"""

        if file_chain_length == None or full_protein_chain_length == None:
            return None
        
        if file_chain_length <= 0 or full_protein_chain_length <= 0:
            return 0
        return file_chain_length / full_protein_chain_length