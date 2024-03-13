import logging
import unittest
import hashlib
logger = logging.getLogger(__name__)

from src.database_entries.afdb_entry import *
logging.getLogger("src.AFDBEntry").setLevel(logging.ERROR) # Disable warnings in PDBeEntry class
test_entry = AFDBEntry({'id': 'P02070'})

class TestAFDBEntry(unittest.TestCase):
    def test_fetching(self):
        self.assertEqual(len(test_entry.fetch()), 96227, "Mismatching lengths")
        self.assertEqual(hashlib.sha256(test_entry.fetch().encode("utf-8")).hexdigest()[:16], "b9d5cede21b982e1", "Invalid .pdb file fetched for P02070 entry (hash mismatch)")

        logger.warning("Paritally Implemented: more thorough fetching tests missing.")

    def test_overall_score_calculation(self):
        test_entry.fetch()
        score = test_entry.calculate_raw_quality_score()
        self.assertEqual(score, 0, f"Incorrect quality score calculated for entry {test_entry.entry_data['id']}, expected 1.0, got {score}")
    

if __name__ == "__main__":
    unittest.main()
