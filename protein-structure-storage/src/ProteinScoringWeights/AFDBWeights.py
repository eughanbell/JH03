import logging
logger = logging.getLogger(__name__)

from . import __all_scores

MASTER_WEIGHT = __all_scores.get("PDBe", {}).get("MASTER_WEIGHT", {})
# RELATIVE_WEIGHTS = __all_scores.get("PDBe", {}).get("RELATIVE_WEIGHTS", {})
# METHOD_WEIGHTS = __all_scores.get("PDBe", {}).get("METHOD_WEIGHTS", {})
# RESOLUTION_WEIGHTS = __all_scores.get("PDBe", {}).get("RESOLUTION_WEIGHTS", {})

if not MASTER_WEIGHT:
    logger.critical("Cannot perform protein scoring: PDBe section of scoring file corrupted.")