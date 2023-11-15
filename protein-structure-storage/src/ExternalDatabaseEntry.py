class ExternalDatabaseEntry:
    """ Represents an entry in an external database. """

    def __init__(self, entry_data:dict):
        self.entry_data = entry_data # Each subclass will have logic for processing it's own entry_data dict
        self.quality_score = None # Quality score from 0 to 1
    
    def fetch(self) -> bytes:
        """ Fetch a .pdb file from external database and return in string format. """
        raise NotImplementedError("External database fetch not implemented.")
    
    def get_quality_score(self, recalculate=False) -> float:
        """ Get the quality score, recalculating it if necessary. """
        if recalculate == True or self.quality_score == None:
            self.calculate_quality_score()
            return self.quality_score
        else:
            return self.quality_score

    def calculate_quality_score(self) -> float:
        """ Calculate quality score for this entry """
        raise NotImplementedError("Quality score calculator not implemented.")