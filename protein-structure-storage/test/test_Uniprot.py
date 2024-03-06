import logging
import json
import unittest
logger = logging.getLogger(__name__)

from urllib.request import urlopen

from src.uniprot import _request_uniprot_file
from src.uniprot import _parse_uniprot_xml
from src.uniprot import uniprot_get_entries

class TestUniprot(unittest.TestCase):
    def test__request_uniprot_file(self):
        #Valid A
        validTest = _request_uniprot_file("p02070","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p02070.xml")
        self.assertEqual(validTest, comparison.read())
        
        #Valid B
        validTest = _request_uniprot_file("p06213","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p06213.xml")
        self.assertEqual(validTest, comparison.read())

        #Valid C
        validTest = _request_uniprot_file("a0pk11","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/a0pk11.xml")
        self.assertEqual(validTest, comparison.read())

        #Invalid uniprot_id
        self.assertEqual(_request_uniprot_file("ImNotAnId", "xml"), None)

        #Invalid filetype
        self.assertEqual(_request_uniprot_file("p02070", "ImNotAFiletype"), None)

        #Invalid filetype
        self.assertEqual(_request_uniprot_file("p02070", None), None)

        #Non-string uniprot_id
        self.assertEqual(_request_uniprot_file(2070, "xml"), None)

        #Non-xml filetype
        self.assertEqual(_request_uniprot_file("p02070", "html"), None)

    def test_parse_uniprot_xml(self):
        path = "test/testdata/uniprot"
        test_cases = [ # List of uniprot_id, expected_output_file tuples
            ("A0A7M7QR98", f"{path}/A0A7M7QR98.json"),
            ("Q9NR00", f"{path}/Q9NR00.json"),
            ("P00022", f"{path}/P00022.json"),
            ("ImNotAnId", None), # Invalid uniprot_id
            (2000, None), # Non-string uniprot_id
        ]

        for uniprot_id, expected_output_file in test_cases:
            actual_output = _parse_uniprot_xml(uniprot_id)
            if expected_output_file == None:
                self.assertEqual(actual_output, [], f"Parser incorrectly handled invalid uniprot_id {uniprot_id}.")
            else:
                for test_case in ["external_db_name", "id"]:
                    for elem in actual_output:
                        self.assertNotEqual(elem.get(test_case,None), None, f"Parser incorrectly handled valid uniprot file {uniprot_id}, '{test_case}' attribute did not exist.")
                        self.assertNotEqual(elem.get(test_case,""), "", f"Parser incorrectly handled valid uniprot file {uniprot_id}, '{test_case}' attribute is empty.")
                for test_case in ["mass","sequence","sequence_length"]:
                    for elem in actual_output:
                        self.assertNotEqual(elem["protein_metadata"].get(test_case,None), None, f"Parser incorrectly handled valid uniprot file {uniprot_id}, '{test_case}' attribute did not exist.")
                        self.assertNotEqual(elem["protein_metadata"].get(test_case,""), "", f"Parser incorrectly handled valid uniprot file {uniprot_id}, '{test_case}' attribute is empty.")

if __name__ == "__main__":
    unittest.main()
