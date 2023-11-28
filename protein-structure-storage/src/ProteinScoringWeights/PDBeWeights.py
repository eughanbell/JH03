import logging
logger = logging.getLogger(__name__)

from . import __all_scores

method_weights_raw = __all_scores.get("PDBe", {}).get("METHOD_WEIGHTS", {})

MASTER_WEIGHT = __all_scores.get("PDBe", {}).get("MASTER_WEIGHT", {})
RELATIVE_WEIGHTS = __all_scores.get("PDBe", {}).get("RELATIVE_WEIGHTS", {})
CHAIN_LENGTH_WEIGHTS = __all_scores.get("PDBe", {}).get("CHAIN_LENGTH_WEIGHTS", {})
METHOD_WEIGHTS = {key.lower():value for key, value in method_weights_raw.items()} # METHOD_WEIGHTS must be converted to lower case
RESOLUTION_WEIGHTS = __all_scores.get("PDBe", {}).get("RESOLUTION_WEIGHTS", {})


if not MASTER_WEIGHT or not RELATIVE_WEIGHTS or not CHAIN_LENGTH_WEIGHTS or not METHOD_WEIGHTS or not RESOLUTION_WEIGHTS:
    logger.critical("Cannot perform protein scoring: PDBe section of ProteinScoringWeights.yaml corrupted.")