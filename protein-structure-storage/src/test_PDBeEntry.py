import logging
import unittest
logger = logging.getLogger(__name__)

from PDBeEntry import PDBeEntry

test_entry = PDBeEntry({'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145'})

class TestPDBeEntry(unittest.TestCase):    
    def test_resolution_extraction(self):
        test_entry.entry_data["resolution"] = "1.34 A" # Valid float
        self.assertEqual(test_entry.extract_resolution(), 1.34, "Failed to handle float import")

        test_entry.entry_data["resolution"] = "7 A" # Valid int
        self.assertEqual(test_entry.extract_resolution(), 7, "Failed to handle int import")

        test_entry.entry_data["resolution"] = "1.34a A" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "1.34" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "1.34a A" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

        test_entry.entry_data["resolution"] = "" # Invalid
        self.assertEqual(test_entry.extract_resolution(), None)

    def test_method_extraction(self):
        test_entry.entry_data["method"] = "X-ray" # Valid method
        self.assertEqual(test_entry.extract_method(), "X-ray")

        logger.warning("Partially implemented: need to implement more tests for extracting valid methods")

        test_entry.entry_data["method"] = "" # Invalid
        self.assertEqual(test_entry.extract_method(), None)

    def test_chain_length_extraction(self):
        test_entry.entry_data["chains"] = "B/D=1-145"
        self.assertEqual(test_entry.extract_chain_length(), 145, "Failed to extract chain length")

        test_entry.entry_data["chains"] = "B/D=73-100"
        self.assertEqual(test_entry.extract_chain_length(), 28, "Failed to extract chain length")

        test_entry.entry_data["chains"] = "C/E=73-100"
        self.assertEqual(test_entry.extract_chain_length(), 28, "Failed to extract chain length")

        test_entry.entry_data["chains"] = "C/E=100-73" # Invalid data (unlikely to be in DB, but worth checking this edge case)
        self.assertEqual(test_entry.extract_chain_length(), None, "Imported invalid chain length")

        test_entry.entry_data["chains"] = "" # Invalid
        self.assertEqual(test_entry.extract_chain_length(), None)

        test_entry.entry_data["chains"] = "B/D73-100" # Invalid
        self.assertEqual(test_entry.extract_chain_length(), None)

        test_entry.entry_data["chains"] = "B/D=73100" # Invalid
        self.assertEqual(test_entry.extract_chain_length(), None)

    def test_resolution_score_calculation(self):
        logger.warning("Resolution scoring testing incomplete.")
        self.assertEqual(test_entry.calculate_resolution_score(0.0), 1) # Perfect resolution, score should be 1
        self.assertEqual(test_entry.calculate_resolution_score(1.0), 0.9) # 1A, score should be 0.9
        logger.warning("Resolution scoring testing currently uses hardcoded test values. Correct this before final release.")

        self.assertEqual(test_entry.calculate_resolution_score(None), None) # No resolution, should return None, but not throw error

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