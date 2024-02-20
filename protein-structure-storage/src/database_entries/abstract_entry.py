class ExternalDatabaseEntry:
    """ Represents an entry in an external database.
    Override this class and provide implementations of fetch and score,
    then add this new database entry object to the dict at the top of uniprot.py
    to use as source for protein files."""

    def __init__(self, entry_data:dict):
        self.entry_data = entry_data # Each subclass will have logic for processing it's own entry_data dict
        self.quality_score = None # Quality score from 0 to 1
        self.type = self.__class__.__name__
    
    def fetch(self):
        """ Fetch a .pdb file from external database and return it. """
        raise NotImplementedError("External database fetch not implemented.")
    
    def get_quality_score(self, recalculate=False) -> float:
        """ Get the quality score, recalculating it if necessary. """

        if recalculate == True or self.quality_score == None:
            self.quality_score = self.calculate_raw_quality_score()
        
        return self.quality_score

    def calculate_raw_quality_score(self) -> float:
        """ Calculate quality score for this entry """
        raise NotImplementedError("Quality score calculator not implemented.")
    
    def __lt__(self, other): # Sorting / comparision is based on quality score
        return self.get_quality_score() < other.get_quality_score()
    
    def __repr__(self):
        return f"{self.entry_data}: {self.get_quality_score()}"

    def get_protein_metadata(self) -> dict:
        return self.entry_data["protein_metadata"]

    def get_entry_data(self, field):
        return self.entry_data[field]

