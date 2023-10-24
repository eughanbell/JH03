from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL


class AlphaFoldRequest:

    def __init__(self, uniprot_accession):
        self.uniprot_accession = uniprot_accession

    def generate_request(self) -> str:
        """ Creates a html request for this id"""
        return "https://alphafold.ebi.ac.uk/prediction/" + str(self.uniprot_accession)

    def request_all_models(self):
        """To Do: sends html request for all alphafold models with the given id"""
        f = urlopen(self.generate_request())
        return f.read()


if __name__ == "__main__":
    test = AlphaFoldRequest("P00520")
    print(type(test.request_all_models()))

