from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL
import xml.etree.ElementTree as et
from helpers import get_from_url
import ExternalDatabaseEntry as EDBentry
import PDBeEntry
# list of databases used when found in uniprot
# each entry contains a name which is used in uniprot as 'type'
# and a dbobj which is the type of the ExternalDatabaseEntry object
# that represents that databse
EXTERNAL_DATABASES = (
    # TODO: Add concerte DbEntry objects for these
    {"name": "PDB", "dbobj": PDBeEntry.PDBeEntry},
    {"name": "AlphaFoldDB", "dbobj": EDBentry.ExternalDatabaseEntry}
)


def request_uniprot_file(uniprot_id, filetype):
    """given a uniprot id and file type, both as strings,
    return the text contents of the uniport entry"""
    if not isinstance(uniprot_id, str):
        print("the uniport id was not a string")
        return None
    result = get_from_url("https://rest.uniprot.org/uniprotkb/" +
                          uniprot_id + "." + filetype)
    if result is None:
        print("couldn't fulfil uniport request, id may be invalid" +
              " or there may be a network issue")
    return result


def parse_uniprot_xml(uniprot_id):
    """returns a list of dictionaries containing
    the 'type' (databse name) 'id', databse id
    and 'params' (list of parameters for that entry)
    for all the entries stored by uniport"""
    entries = list()
    xml_text = request_uniprot_file(uniprot_id, "xml")
    if xml_text is None:
        return entries
    root = et.fromstring(xml_text)
    for child in root:
        if child.tag.endswith("entry"):
            for dbentry in child:
                if dbentry.tag.endswith("dbReference"):
                    e = {}
                    e['dbname'] = dbentry.attrib['type']
                    e['dict'] = {}
                    e['dict']['id'] = dbentry.attrib['id']
                    for properties in dbentry:
                        if properties.tag.endswith("property"):
                            e['dict'][properties.attrib['type']] = properties.attrib['value']
                    entries.append(e)
    return entries


def uniprot_get_entries(uniprot_id, uniprot_retrieve_fn=parse_uniprot_xml):
    """Get list of DBEntry Objects for the supported databases
    using a uniprot id"""
    dbrefs = uniprot_retrieve_fn(uniprot_id)
    objs = list()
    for entry in dbrefs:
        for db in EXTERNAL_DATABASES:
            if entry['dbname'] == db['name']:
                objs.append(db['dbobj'](entry['dict']))
                print(f"\ncreating dbentry for {entry['dbname']} database")
                print(entry['dict'])
    return objs


if __name__ == "__main__":
    x = uniprot_get_entries("p01966")
    print(x[0])
    print("=========================")
    print(x[0].fetch())
    # uniprot_get_entries("Q14676")
    # uniprot_get_entries("p0207")
    # uniprot_get_entries("p02 07")
    # uniprot_get_entries(10)