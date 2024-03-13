from enum import Enum
from io import StringIO
import json
import logging
import os
import time

ALPHAFOLD_PATH = "/home/ubuntu/alphafold"

main_logger = logging.getLogger(__name__)

class CalculationManager:

    calculations_list = []

    @classmethod
    def list_calculations(cls):
        return f"[{','.join([str(elem) for elem in cls.calculations_list])}]"

    @classmethod
    def add_calculation(cls, sequence: str):
        for calculation in cls.calculations_list:
            if calculation.sequence == sequence:
                err = f"Cannot enqueue calculation: protein sequence already in calculations list. Sequence: '{sequence}'."
                main_logger.warning(err)
                return json.dumps({"detail":err})
        cls.calculations_list.append( CalculationManager(sequence=sequence) )
    
    @classmethod
    def cancel_calculation(cls, sequence: str):
        for idx, calculation in enumerate(cls.calculations_list):
            if calculation.sequence == sequence:
                if calculation.status == CalculationState.CALCULATING:
                    main_logger.warning("CODE FOR KILLING ONGOING CALCULATION NONEXISTENT!")
                    return json.dumps({"detail":"Could not cancel protein sequence calculation: code for killing ongoing calculation nonexistent."})
                main_logger.info(f"Removing enqueued protein calculation for protein sequence: '{sequence}'.")
                cls.calculations_list.pop(idx)
                return
        err = f"Could not cancel protein sequence calculation: sequence not currently in queue. Sequence: '{sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})
    
    @classmethod
    def download_calculation_result(cls, search_sequence: str, download_options: str):
        for elem in cls.calculations_list:
            if elem.sequence == search_sequence:
                if elem.status == CalculationState.COMPLETE:
                    return elem.getResults(download_options)

                if elem.status == CalculationState.FAILED:
                    return elem.logs
                else:
                    err = f"Cannot download result: calculation is still in the {elem.status} state."
                    main_logger.warning(err)
                    return json.dumps({"detail":err})
        err = f"Cannot download result: not currently processing protein sequence'{search_sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})

class CalculationState(Enum):
    WAITING = 0
    CALCULATING = 1
    COMPLETE = 2
    FAILED = 3

    def __str__(self):
        return self.name