from .helpers import get_from_url, query_list_path
from .uniprot import uniprot_get_entries, resolve_aliases
import json
import logging
import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)

# docker compose internal protein cache url
CACHE_CONTAINER_URL = "http://pc:6000"


def upload_pdb_file(text, source_db, uniprot_id="", sequence="", score=0):
    r = requests.post(CACHE_CONTAINER_URL + "/protein_file",
                      json={"uniprot_id": uniprot_id,
                            "pdb_file": text,
                            "sequence": sequence,
                            "source_db": source_db,
                            "score": score})
    if r.status_code != 200:
        logger.error(f"Failed to store protein file in cache: {r.text}")
    return r.text


def get_pdb_file(uniprot_id, override_cache=False, source_dbs=None):
    """
    return a pdb_file from cache or from an external database
    matching the uniprot id.
    source_dbs can be a list of databases to check.
    By default it will use all implemented databases.
    """
    if source_dbs is None:
        source_dbs = []
    else:
        source_dbs = resolve_aliases(source_dbs)
    protein_file = ""
    if not override_cache:
        protein_file = _request_from_cache(
            uniprot_id, "/retrieve_by_uniprot_id/",
            query=query_list_path("source_dbs", source_dbs)
        )
    if protein_file == "":
        # check uniprot if file not in cache
        entries = uniprot_get_entries(
            uniprot_id, source_dbs=source_dbs)
        
        if len(entries) == 0:
            logger.warning(
                f"No proteins found in UniProt database, id: {uniprot_id}")
            return ""
        else:
            entries.sort(reverse=True)
            logger.info(f"Considered {len(entries)} entries, "
                        + f"choosing best. id: {uniprot_id} - db: "
                        + f"{entries[0].get_entry_data('external_db_name')}")
            print(entries[0])
            protein_file = entries[0].fetch()
            try:
                upload_pdb_file(
                    protein_file,
                    entries[0].get_entry_data("external_db_name"),
                    uniprot_id,
                    entries[0].get_protein_metadata()["sequence"],
                    entries[0].get_quality_score())
            except ConnectionError as e:
                print(e)
    return protein_file


def get_pdb_file_by_sequence(sequence):
    return _request_from_cache(sequence, "/retrieve_by_sequence/")


def get_pdb_file_by_db_id(db_id):
    return _request_from_cache(db_id, "/retrieve_by_db_id/")


def get_db_id_by_uniprot_id(uniprot_id):
    """
    returns the database id of the pdb file with the matching uniprot id
    if that uniprot id is not in the local cache, then first add it to cache
    """
    db_id = _request_from_cache(
        uniprot_id, "/retrieve_db_id_by_uniprot_id/", field="db_id")
    if db_id == "":
        if get_pdb_file(uniprot_id) != "":
            db_id = _request_from_cache(
                uniprot_id, "/retrieve_db_id_by_uniprot_id/", field="db_id")
    return db_id



# --------------------------------------------------------
# --------------- PRIVATE HELPER FUNCTIONS ---------------
# --------------------------------------------------------


def _request_from_cache(search_value, cache_endpoint, query="", field="pdb_file"):
    logger.info(f"Attempting fetch from cache {cache_endpoint} - looking for {search_value}.")
    f = get_from_url(CACHE_CONTAINER_URL
                     + cache_endpoint
                     + search_value
                     + query)
    if f is None:
        logger.error("Network issue while fetching protein file from cache.")
        return ""
    response = json.loads(f)
    if not response['present']:
        logger.info("Cache miss.")
        return ""
    logger.info(f"Cache hit, returning requested field {field}.")
    return response[field]
