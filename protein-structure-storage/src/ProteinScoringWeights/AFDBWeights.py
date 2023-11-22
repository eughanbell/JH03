import logging
logger = logging.getLogger(__name__)

from . import __all_scores

MASTER_WEIGHT = __all_scores.get("AFDB", {}).get("MASTER_WEIGHT", None)

if MASTER_WEIGHT == None:
    logger.critical("Cannot perform protein scoring: AFDB section of scoring file corrupted.")