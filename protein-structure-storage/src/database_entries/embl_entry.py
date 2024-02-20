from .abstract_entry import ExternalDatabaseEntry
from ..helpers import get_from_url

class EMBLEntry(ExternalDatabaseEntry):
    
    def fetch(self):
        embl_id = self.entry_data["id"]
        embl_url = f"https://www.ebi.ac.uk/ena/browser/api/embl/{embl_id}"
        return get_from_url(embl_url).decode()
    
    def calculate_raw_quality_score(self):
        score = 0
        molecule_type = self.entry_data["molecule type"]
        if molecule_type == "mRNA":
            score = 0.4
        elif molecule_type == "Genomic DNA":
            score = 0.2
        else:
            score = 0.1
        return score
