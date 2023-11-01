from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL


class AlphaFoldRequest:

    def __init__(self, uniprot_accession):
        self.uniprot_accession = uniprot_accession

    def request_pdb(self) -> bytes:
        """Sends html request for all alphafold pdb file with the given id.
        To Do: add error handling."""
        alphafold_id = "AF-" + self.uniprot_accession + "-F1"
        database_version = 'v4'
        model_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{database_version}.pdb'
        f = urlopen(model_url)
        return f.read()
