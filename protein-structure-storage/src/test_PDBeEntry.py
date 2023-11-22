import logging
import unittest
logger = logging.getLogger(__name__)

from PDBeEntry import PDBeEntry
from ProteinScoringWeights.PDBeWeights import *

test_entry = PDBeEntry({'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145', 'protein_metadata': {'mass':15389, 'sequence_length':145, 'sequence': 'MVLSAADKGNVKAAWGKVGGHAAEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGAKVAAALTKAVEHLDDLPGALSELSDLHAHKLRVDPVNFKLLSHSLLVTLASHLPSDFTPAVHASLDKFLANVSTVLTSKYRPSD'}})

class TestPDBeEntry(unittest.TestCase):    
    def test_resolution_extraction(self):
        test_entry.entry_data["resolution"] = "1.34 A" # Valid float
        self.assertEqual(test_entry.extract_resolution(), 1.34, "Failed to handle float import: 1.34 A ")

        test_entry.entry_data["resolution"] = "7 A" # Valid int
        self.assertEqual(test_entry.extract_resolution(), 7, "Failed to handle int import: 7 A")

        test_entry.entry_data["resolution"] = "1.34a A" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "1.34" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "1.34a A" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

    def test_method_extraction(self):
        test_cases = [ # List of (input, expected_output, error message fragment) tuples
            ("X-ray", "X-ray", "valid input"),
            ("othermethod", "othermethod", "valid input not in weights dictionary"),
            ("", None, "missing method")
        ]
        for test_case in test_cases:
            test_entry.entry_data["method"] = test_case[0]
            val = test_entry.extract_method()
            self.assertEqual(val, test_case[1], f"Failed to parse {test_case[2]}, expected {test_case[1]}, got {val}")

        logger.warning("Partially implemented: need to implement more tests for extracting valid methods")

    def test_chain_length_extraction(self):
        test_cases = [ # List of (input, expected_output) tuples
            ("B/D=1-145", 145),
            ("B/D=73-100", 28),
            ("C/E=73-100", 28),
            ("C/E=100-73", 28), # Reverse ordering should still give positive value
            ("F=73-100", 28),
            ("A=1-23, B=50-79", 53),
            ("A=1-23,B=50-79", 53),
            ("A=1-23,       B=50-79", 53),
            ("A/B=1-23, C/D=50-79", 53),
            ("A=1-23, C/D=50-79", 53),
            ("A/B=1-23, D=50-79", 53),
            # Invalid / partially cases
            ("", None),
            ("B/D73-100", None),
            ("A=1, B=3", None),
            ("B/D=73100", None),
            ("A=1-28, B=3", 28),
        ] 
        for test_case in test_cases:
            test_entry.entry_data["chains"] = test_case[0]
            self.assertEqual(test_entry.extract_chain_length(), test_case[1], f"Failed to extract chain length from {test_case[0]}")

    def test_full_chain_length_extraction(self):
        logger.warning("Not Implemented: extraction of full protein chain length from metadata.")
        test_cases = [ # List of (protein metadata dict, expected output, error message fragment) tuples
            ({"sequence":"", "sequence_length":"0"}, 0, "0-length input"),
            ({"sequence":"A", "sequence_length":"1"}, 1, "1-length input"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":"12"}, 12, "input"),
            ({"sequence":"", "sequence_length":"12"}, 12, "missing sequence data"),
            ({"sequence":"DKAMFOWEMVLA"}, 12, "missing reported sequence length data"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":"na"}, 12, "corrupted reported sequence length data"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":""}, 12, "corrupted reported sequence length data"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":"0"}, 12, "mismatch between sequence and reported sequence length"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":"10"}, 12, "mismatch between sequence and reported sequence length"),
            ({"sequence":"DKAMFOWEMVLA", "sequence_length":"20"}, 20, "mismatch between sequence and reported sequence length"),
            ({"sequence":"PQRMCUWEXI"*1000, "sequence_length":"10000"}, 10_000, "large input"),
            ({"sequence":"PQRMCUWEXI"*10000, "sequence_length":"100000"}, 100_000, "very large input"),
        ]

        for test_case in test_cases:
            test_entry.entry_data["protein_metadata"] = test_case[0]
            val = test_entry.extract_full_chain_length()
            self.assertEqual(val, test_case[1], f"Failed to handle {test_case[2]}, expected {test_case[1]}, got {val}.")

    def test_resolution_score_calculation(self):
        DEFAULT = RESOLUTION_WEIGHTS["default_score"]
        logger.warning("Resolution scoring testing incomplete.")
        self.assertEqual(test_entry.calculate_resolution_score(0.0), 1) # Perfect resolution, score should be 1
        self.assertEqual(test_entry.calculate_resolution_score(1.0), 0.9) # 1 angstrom, score should be 0.9
        logger.warning("Resolution scoring testing currently uses hardcoded test values. Correct this before final release.")

        self.assertEqual(test_entry.calculate_resolution_score(None), DEFAULT, f"Failed to return default value on invalid resolution data.")

    def test_method_score_calculation(self):
        logger.warning("Not Implemented: method scoring tests not implemented")

    def test_chain_length_score_calculation(self):
        logger.warning("Not Implemented: chain length scoring tests.")

    def test_overall_score_calculation(self):
        logger.warning("Not Implemented: Overall scoring tests.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.warning("NotImplemented: no tests for PDBeFetch.")
    unittest.main()