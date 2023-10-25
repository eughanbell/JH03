import ExternalDatabaseEntry

class PDBeEntry(ExternalDatabaseEntry):
    def __init__(self, entry_data):
        super()
    
    def fetch(self) -> str:
        """ Fetch a .pdb file from PDBe database and return in string format. """
        raise NotImplementedError("PDBe fetch not implemented.")
    
    def quality_score(self) -> float:
        """ Calculate quality score for this entry """
        pass