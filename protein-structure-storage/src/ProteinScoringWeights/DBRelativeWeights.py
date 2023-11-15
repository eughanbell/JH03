import logging
logger = logging.getLogger(__name__)

from . import __all_scores

PDBE_RELATIVE_WEIGHT = __all_scores.get("PDBe", {}).get("MASTER_WEIGHT", None)
AFDB_RELATIVE_WEIGHT = __all_scores.get("AFDB", {}).get("MASTER_WEIGHT", None)

if not PDBE_RELATIVE_WEIGHT or not AFDB_RELATIVE_WEIGHT:
    logger.critical("Cannot perform protein scoring: master database weights part of ProteinScoringWeights.yaml corrupted.")