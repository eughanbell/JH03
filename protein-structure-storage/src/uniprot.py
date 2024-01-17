from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL
import logging
from xml.etree import ElementTree

from .helpers import get_from_url
from . import PDBeEntry, AFDBEntry

logger = logging.getLogger(__name__)

# Mappings of external database names to their corresponding
# ExternalDatabaseEntry objects, which are used to represent
# entries in that database.

EXTERNAL_DATABASES = {
    # TODO: Add concrete DbEntry objects for these
    "PDB": PDBeEntry.PDBeEntry,
    "AlphaFoldDB": AFDBEntry.AFDBEntry
}


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
                    new_entry['external_database_name'] = dbentry.attrib['type']
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


def uniprot_get_entries(uniprot_id, uniprot_retrieval_function=parse_uniprot_xml):
    """ Get list of ExternalDatabaseEntry objects for the supported databases
    using a uniprot id. """
    uniprot_entries_data = uniprot_retrieval_function(uniprot_id)
    entries = list()
    for entry_data in uniprot_entries_data:
        database_object = EXTERNAL_DATABASES.get(entry_data["external_database_name"])
        if database_object:
            entries.append(database_object(entry_data))
    return entries
