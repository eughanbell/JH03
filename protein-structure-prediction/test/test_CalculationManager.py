import logging
import unittest

from src.CalculationManager import CalculationManager

logger = logging.getLogger(__name__)

class TestCalculationManager(unittest.TestCase):
    def test_list_calculations(self):
        self.assertEqual(CalculationManager.list_calculations(), "[]", "Mishandled no calculations state.")
        logger.warning("Tests incomplete for PSP Container.")
        logger.warning("Tests incomplete for CalculationManager.")
        logger.warning("Tests incomplete for list_calculations.")
    
if __name__ == "__main__":
    unittest.main()
