import logging
logger = logging.getLogger(__name__)

from . import __all_scores

MASTER_WEIGHT = __all_scores.get("AFDB", {}).get("MASTER_WEIGHT", {})
# RELATIVE_WEIGHTS = __all_scores.get("AFDB", {}).get("RELATIVE_WEIGHTS", {})
# METHOD_WEIGHTS = __all_scores.get("AFDB", {}).get("METHOD_WEIGHTS", {})
# RESOLUTION_WEIGHTS = __all_scores.get("AFDB", {}).get("RESOLUTION_WEIGHTS", {})

if not MASTER_WEIGHT:
    logger.critical("Cannot perform protein scoring: AFDB section of scoring file corrupted.")