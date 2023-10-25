from ExternalDatabaseEntry import ExternalDatabaseEntry

# {'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145'}

class PDBeEntry(ExternalDatabaseEntry):

    def fetch(self) -> str:
        """ Fetch a .pdb file from PDBe database and return in string format. """
        raise NotImplementedError("PDBe fetch not implemented.")

    def calculate_quality_score(self):
        """ Fetch or calculate quality score for this entry """
        pass
