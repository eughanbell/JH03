import logging
import os
import yaml

logger = logging.getLogger(__name__)

def __get_scores_from_yaml():
    try:
        fpath = os.path.abspath(f'{__file__}/../../../settings/ProteinScoringWeights.yaml')
        with open(fpath, 'r') as yaml_file:
            all_scores = yaml.safe_load(yaml_file)
        return all_scores
    except FileNotFoundError:
        logger.critical("Cannot perform protein scoring: Could not find ProteinScoringWeights.yaml in protein-structure-storage/settings. Please create this file.")
        return {}
    
__all_scores = __get_scores_from_yaml()

from . import PDBeWeights
from . import AFDBWeights
from . import DBRelativeWeights