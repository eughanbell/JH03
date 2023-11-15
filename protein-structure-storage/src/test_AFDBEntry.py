import logging
import unittest
import hashlib
logger = logging.getLogger(__name__)

from AFDBEntry import AFDBEntry

class TestAFDBEntry(unittest.TestCase):
    def test_fetching(self):
        def get_output(metadata_dict):
            test_entry = AFDBEntry(metadata_dict)
            return test_entry.fetch()
        self.assertEqual(len(get_output({'id': 'P02070'})), 96227, "Mismatching lengths")
        self.assertEqual(hashlib.sha256(get_output({'id': 'P02070'})).hexdigest()[:16], "b9d5cede21b982e1", "Invalid .pdb file fetched for P02070 entry (hash mismatch)")

        logger.warning("Paritally Implemented: more thorough fetching tests missing.")

    def test_overall_score_calculation(test_entry):
        logger.warning("Not Implemented: overall scoring tests.")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()