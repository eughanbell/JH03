from .helpers import get_from_url
from .uniprot import uniprot_get_entries
import json
import requests

# docker compose internal protein cache url
CACHE_CONTAINER_URL = "http://pc:6000"

def request_from_cache(search_value, cache_endpoint):
    f = get_from_url(CACHE_CONTAINER_URL
                     + cache_endpoint
                     + search_value)
    if f is None:
        print("Error: Network issue when requesting protein file from cache")
        return None
    response = json.loads(f)
    if not response['present']:
        return None
    return response['pdb_file']


def get_pdb_file(uniprot_id):
    protein_file = request_from_cache(uniprot_id, "/retrieve_by_uniprot_id/")
    if protein_file is None:
        # check uniprot if file not in cache
        entries = uniprot_get_entries(uniprot_id)
        if len(entries) == 0:
            print("Error: no proteins found in uniprot database, "
                  + f"id: {uniprot_id}")
            return ""
        else:
            entries.sort(reverse=True)
            protein_file = entries[0].fetch()
        
            r = requests.post(CACHE_CONTAINER_URL + "/protein_file",
                              json={"uniprot_id": uniprot_id,
                                    "pdb_file": protein_file,
                                    "sequence":
                                    entries[0]
                                    .get_protein_metadata()["sequence"]})
            if r.status_code != 200:
                print(f"Failed to store protein file in cache: {r.text}")
    return protein_file


def get_pdb_file_by_sequence(sequence):
    return request_from_cache(sequence, "/retrieve_by_sequence/")
        

#print(get_pdb_file('p02070'))
