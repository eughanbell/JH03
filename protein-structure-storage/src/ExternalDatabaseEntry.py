class ExternalDatabaseEntry:
    """ Represents an entry in an external database. """

    def __init__(self, entry_data:dict):
        self.entry_data = entry_data # Each subclass will have logic for processing it's own entry_data dict
        self.quality_score = 0 # Quality score from 0 to 1
    
    def fetch(self) -> str:
        """ Fetch a .pdb file from external database and return in string format. """
        raise NotImplementedError("External database fetch not implemented.")
    
    def quality_score(self) -> float:
        """ Calculate quality score for this entry """
        raise NotImplementedError("Quality score calculator not implemented.")