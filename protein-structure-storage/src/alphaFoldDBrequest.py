from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL


class AlphaFoldRequest:

    def __init__(self, uniprot_accession):
        self.uniprot_accession = str(uniprot_accession)

    def request_pdb(self) -> bytes:
        """Sends html request for all alphafold pdb file with the given id."""
        alphafold_id = "AF-" + self.uniprot_accession + "-F1"
        database_version = 'v4'
        model_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{database_version}.pdb'
        try:
            f = urlopen(model_url)
            if f.getcode() == 200:
                return f.read()
            else:
                raise HTTPError(model_url, 404, "File not found")
        except Exception as e:
            raise Exception(e)
