import logging
import json
import unittest
logger = logging.getLogger(__name__)

from urllib.request import urlopen

from src.uniprot import request_uniprot_file
from src.uniprot import parse_uniprot_xml
from src.uniprot import uniprot_get_entries

class TestUniprot(unittest.TestCase):
    def test_request_uniprot_file(self):
        #Valid A
        validTest = request_uniprot_file("p02070","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p02070.xml")
        self.assertEqual(validTest, comparison.read())
        
        #Valid B
        validTest = request_uniprot_file("p06213","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p06213.xml")
        self.assertEqual(validTest, comparison.read())

        #Valid C
        validTest = request_uniprot_file("a0pk11","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/a0pk11.xml")
        self.assertEqual(validTest, comparison.read())

        #Invalid uniprot_id
        self.assertEqual(request_uniprot_file("ImNotAnId", "xml"), None)

        #Invalid filetype
        self.assertEqual(request_uniprot_file("p02070", "ImNotAFiletype"), None)

        #Non-string uniprot_id
        self.assertEqual(request_uniprot_file(2070, "xml"), None)

        #Non-xml filetype
        self.assertEqual(request_uniprot_file("p02070", "html"), None)

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
            actual_output = parse_uniprot_xml(uniprot_id)
            if expected_output_file == None:
                self.assertEqual(actual_output, [], f"Parser incorrectly handled invalid uniprot_id {uniprot_id}.")
            else:
                try:
                    with open(expected_output_file) as file:
                        expected_output = json.load(file)
                        self.assertEqual(actual_output, expected_output, f"Failed to parse XML for uniprot_id {uniprot_id}.")
                except FileNotFoundError:
                    self.fail(f"Missing test case file {expected_output_file}!")

if __name__ == "__main__":
    unittest.main()
