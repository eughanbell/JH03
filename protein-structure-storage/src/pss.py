from .helpers import get_from_url
from .uniprot import uniprot_get_entries
import json
import requests

# docker compose internal protein cache url
CACHE_CONTAINER_URL = "http://pc:6000"


def request_from_cache(search_value, cache_endpoint, field="pdb_file"):
    f = get_from_url(CACHE_CONTAINER_URL
                     + cache_endpoint
                     + search_value)
    if f is None:
        return ""
    response = json.loads(f)
    if not response['present']:
        return ""
    return response[field]


def get_pdb_file(uniprot_id):
    protein_file = request_from_cache(uniprot_id, "/retrieve_by_uniprot_id/")
    if protein_file == "":
        # check uniprot if file not in cache
        entries = uniprot_get_entries(uniprot_id)
        if len(entries) == 0:
            print(f"no entry with id `{uniprot_id}` found in uniprot database")
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


def get_pdb_file_by_db_id(db_id):
    return request_from_cache(db_id, "/retrieve_by_db_id/")


# return the database id of the pdb file with the matching uniprot id
# if that uniprot id is not in the local cache, then first add it to cache
def get_db_id_by_uniprot_id(uniprot_id):
    db_id = request_from_cache(uniprot_id, "/retrieve_db_id_by_uniprot_id/", field="db_id")
    if db_id == "":
        if get_pdb_file(uniprot_id) != "":
            db_id = request_from_cache(uniprot_id,
                                       "/retrieve_db_id_by_uniprot_id/",
                                       field="db_id")
    return db_id
