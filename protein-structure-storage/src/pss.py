from helpers import get_from_url
from uniprot import uniprot_get_entries
import json 

def request_from_cache(uniprot_id):
    f = get_from_url("http://0.0.0.0:6000/retrieve_by_uniprot_id/" + uniprot_id)
    if f is None:
        print("Error: Network issue when requesting protein file from cache")
        return None
    response = json.loads(f.read())
    if not response['present']:
        return None
    # TODO: this doesnt mean anything yet
    return response['file']

def get_pdb_file(uniprot_id):
    protein_file = request_from_cache(uniprot_id)
    if protein_file is not None:
        return protein_file
    entries = uniprot_get_entries(uniprot_id)
    entries.sort(key= lambda entry : entry.calculate_quality_score(), reverse=True)
    pdb_file = entries[0].fetch()
    #TODO: send to pc before returning
    return pdb_file
    

# error right now as score functions not implemented yet
get_pdb_file("P02070")
