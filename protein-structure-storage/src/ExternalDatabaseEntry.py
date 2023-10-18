class ExternalDatabaseEntry:
    """ Represents an entry in an external database. """

    def __init__(self, internal_database_id:str):
        self.internal_database_id = internal_database_id
        self.quality_score = 0
    
    def fetch(self) -> str:
        """ Fetch a .pdb file from external database and return in string format. """
        raise NotImplementedError("External database fetch not implemented.")
    
    def quality_score(self) -> float:
        """ Calculate quality score for this entry """
        raise NotImplementedError("Quality score calculator not implemented.")