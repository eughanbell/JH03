from .helpers import get_from_url
from .uniprot import uniprot_get_entries
import json
import logging
import requests

logger = logging.getLogger(__name__)

# docker compose internal protein cache url
CACHE_CONTAINER_URL = "http://pc:6000"


def request_from_cache(search_value, cache_endpoint, field="pdb_file"):
    logger.info(f"Attempting fetch from cache {cache_endpoint} - looking for {search_value}.")
    f = get_from_url(CACHE_CONTAINER_URL
                     + cache_endpoint
                     + search_value)
    if f is None:
        logger.error("Network issue while fetching protein file from cache.")
        return ""
    response = json.loads(f)
    if not response['present']:
        logger.info("Cache miss.")
        return ""
    logger.info(f"Cache hit, returning requested field {field}.")
    return response[field]

def upload_pdb_file(text, source_db, uniprot_id="", sequence=""):
    r = requests.post(CACHE_CONTAINER_URL + "/protein_file",
                      json={"uniprot_id": uniprot_id,
                            "pdb_file": text,
                            "sequence": sequence,
                            "source_db": source_db})
    if r.status_code != 200:
        logger.error(f"Failed to store protein file in cache: {r.text}")
    return r.text

def get_pdb_file(uniprot_id, override_cache=False, use_dbs={}):
    protein_file = ""
    if not override_cache:
        protein_file = request_from_cache(
            uniprot_id, "/retrieve_by_uniprot_id/")
    if protein_file == "":
        # check uniprot if file not in cache
        entries = uniprot_get_entries(uniprot_id)
        if len(entries) == 0:
            logger.warning(
                f"No proteins found in UniProt database, id: {uniprot_id}")
            return ""
        else:
            entries.sort(reverse=True)
            logger.info(f" Considered {len(entries)} entries, "
                        + f"choosing best. id: {uniprot_id} - db: "
                        + f"{entries[0].get_entry_data('external_db_name')}")
            protein_file = entries[0].fetch()
            upload_pdb_file(
                protein_file,
                entries[0].get_entry_data("external_db_name"),
                uniprot_id,
                entries[0].get_protein_metadata()["sequence"])
    return protein_file


def get_pdb_file_by_sequence(sequence):
    return request_from_cache(sequence, "/retrieve_by_sequence/")


def get_pdb_file_by_db_id(db_id):
    return request_from_cache(db_id, "/retrieve_by_db_id/")


# return the database id of the pdb file with the matching uniprot id
# if that uniprot id is not in the local cache, then first add it to cache
def get_db_id_by_uniprot_id(uniprot_id):
    db_id = request_from_cache(
        uniprot_id, "/retrieve_db_id_by_uniprot_id/", field="db_id")
    if db_id == "":
        if get_pdb_file(uniprot_id) != "":
            db_id = request_from_cache(
                uniprot_id, "/retrieve_db_id_by_uniprot_id/", field="db_id")
    return db_id
