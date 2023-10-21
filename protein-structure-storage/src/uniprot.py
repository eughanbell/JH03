from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import InvalidURL
import xml.etree.ElementTree as et


def request_uniprot_file(uniprot_id, filetype):
    """given a uniprot id and file type, both as strings,
    return the text contents of the uniport entry"""
    if not isinstance(uniprot_id, str):
        print("the supplied uniprot id was not a string")
    else:
        try:
            f = urlopen("https://rest.uniprot.org/uniprotkb/"
                        + uniprot_id + "." + filetype)
            if f.getcode() != 200:
                print(f"http status code: {f.getcode()}, uniprot id"
                      " was invalid, id: {uniprot_id}")
            else:
                return f.read()
        except HTTPError:
            print("HTTP ERORR: uniprot id was invalid, id: " + uniprot_id)
        except InvalidURL:
            print("The uniprot id was invalid, id: " + uniprot_id)
    return None


def parse_uniprot_xml(uniprot_id):
    """returns a list of dictionaries containing
    the 'type' (databse name) and 'id', databse id
    for all the entries stored by uniport"""
    entries = list()
    xml_text = request_uniprot_file(uniprot_id, "xml")
    if xml_text is None:
        return entries
    root = et.fromstring(xml_text)
    for child in root:
        if child.tag.endswith("entry"):
            for entry in child:
                if entry.tag.endswith("dbReference"):
                    entries.append(entry.attrib)
    return entries


def uniprot_get_entries(uniprot_id, uniprot_retrieve_fn=parse_uniprot_xml):
    """Get list of DBEntry Objects for the supported databases
    using a uniprot id"""
    dbrefs = uniprot_retrieve_fn(uniprot_id)
    for r in dbrefs:
        print(r["type"])


uniprot_get_entries("p02070")
uniprot_get_entries("p0207")
uniprot_get_entries("p02 07")
uniprot_get_entries(10)
