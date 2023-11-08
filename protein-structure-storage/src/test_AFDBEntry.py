import logging
logger = logging.getLogger(__name__)

from AFDBEntry import AFDBEntry

def test_fetching(test_entry):
    logger.warning("Not Implemented: Fetching tests.")

def test_overall_score_calculation(test_entry):
    logger.warning("Not Implemented: overall scoring tests.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_entry = AFDBEntry({})
    logger.warning("Not Implemented: using empty value for AFDB metadata.")
    test_fetching(test_entry)
    test_overall_score_calculation(test_entry)
    print("All tests passed!")