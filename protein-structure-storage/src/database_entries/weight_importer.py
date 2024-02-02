import yaml
import logging

logger = logging.getLogger(__name__)

def read_weights(filepath):
    try:
        with open(filepath) as f:
            weights = yaml.safe_load(f)
            return weights
    except Exception as e:
        return {}

def combine_dicts(default, override):
    for k, v in override.items():
        k = k.lower()
        if isinstance(v, dict):
            if default.get(k) == None:
                default[k] = {}
            if isinstance(default.get(k), dict):       
                default[k] = combine_dicts(default[k], v)
            else:
                # ie we expected 'entry: value'
                # but we got 'entry: a: x b: y "
                logging.warning("in weight_importer.py, tried to override "
                                + "a weight that is a value by default "
                                + "with a dictionary")
        else:
            default[k] = v
    return default            

def import_weights(default, filepath):
    combine_dicts(default, read_weights(filepath))
    return default
