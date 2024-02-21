import logging
from xml.etree import ElementTree
from .helpers import get_from_url
from .database_entries import pdbe_entry, afdb_entry

logger = logging.getLogger(__name__)

# Mappings of external database names (in all uppercase, as written in uniprot db)
# to their corresponding
# ExternalDatabaseEntry objects, which are used to represent
# entries in that database.

PDBE_DB_NAME = "PDB".upper()
ALPHAFOLD_DB_NAME = "AlphaFoldDB".upper()

EXTERNAL_DATABASES = {
    PDBE_DB_NAME: pdbe_entry.PDBeEntry,
    ALPHAFOLD_DB_NAME: afdb_entry.AFDBEntry,
}

# Alternate names for supported databases
ALIASES = {
    "AFDB": ALPHAFOLD_DB_NAME,
    "ALPHAFOLD": ALPHAFOLD_DB_NAME,
    "PDBE": PDBE_DB_NAME,
}

def resolve_aliases(source_dbs):
    dbs = []
    for s in source_dbs:
        s = s.upper()
        alias = ALIASES.get(s)
        if alias is None:
            dbs.append(s)
        else:
            dbs.append(alias)
    return dbs


def request_uniprot_file(uniprot_id, filetype):
    """ Given UniProt id and file type strings, return the text contents of
    the UniProt entry. """
    if not isinstance(uniprot_id, str):
        logger.error(f"Failed to fetch UniProt entry, the given UniProt ID was {type(uniprot_id)}, not string")
        return None
    if not isinstance(filetype, str):
        logger.error(f"Failed to fetch UniProt entry, the given filetype was {type(filetype)}, not string")
        return None
    result = get_from_url("https://rest.uniprot.org/uniprotkb/" +
                          uniprot_id + "." + filetype)
    if result is None:
        logger.error("Failed to fetch UniProt entry, id may be invalid or there may be a network issue.")
    logger.info(f"Successfully fetched UniProt entry for {uniprot_id}.")
    return result


def parse_uniprot_xml(uniprot_id):
    """ Return a list of dictionaries containing the 'external_database_name',
    'id' (entry id in the database), 'method', 'resolution', 'chains' and
    'protein_metadata'  (general protein metadata not specific to each database
    entry) for all the entries stored by UniProt. """
    entries = []
    xml_text = request_uniprot_file(uniprot_id, "xml")
    if xml_text is None:
        return entries
    root = ElementTree.fromstring(xml_text)
    extracted_metadata = {} # Any additional metadata that is extracted and stored (this is generic to the protein, not specific to each database entry)
    for child in root:
        if child.tag.endswith("entry"):
            for dbentry in child:
                if dbentry.tag.endswith("dbReference"):
                    new_entry = {}
                    new_entry['external_db_name'] = dbentry.attrib['type']
                    new_entry['id'] = dbentry.attrib['id']
                    for properties in dbentry:
                        if properties.tag.endswith("property"):
                            new_entry[properties.attrib['type']] = properties.attrib['value']
                    entries.append(new_entry)
                elif dbentry.tag.endswith("sequence"):
                    extracted_metadata["sequence"] = dbentry.text
                    extracted_metadata["mass"] = dbentry.attrib['mass']
                    extracted_metadata["sequence_length"] = dbentry.attrib['length']
                    # If we wanted to extract feature metadata,
                    # this could go here

    # Add generic protein metadata to each database entry of this protein
    for entry in entries:
        entry["protein_metadata"] = extracted_metadata
    return entries


def select_external_dbs(source_dbs):
    "Return a subset of EXTERNAL_DATABASES that match the names supplied in the source_dbs list."
    dbs = {}
    for s in source_dbs:
        if EXTERNAL_DATABASES.get(s) is not None:
            dbs[s] = EXTERNAL_DATABASES.get(s)
    return dbs


def uniprot_get_entries(uniprot_id,
                        uniprot_retrieval_function=parse_uniprot_xml,
                        source_dbs=None):
    """ Get list of ExternalDatabaseEntry objects for the supported databases
    using a uniprot id. 
    source_dbs can be a list of database names to consider.
    By default use all implemented databases
    """
    sources = select_external_dbs(source_dbs)
    if source_dbs is None or len(source_dbs) == 0:
        sources = EXTERNAL_DATABASES
    uniprot_entries_data = uniprot_retrieval_function(uniprot_id)
    entries = list()
    for entry_data in uniprot_entries_data:
        database_object = sources.get(entry_data["external_db_name"].upper())
        if database_object:
            entries.append(database_object(entry_data))
    return entries
