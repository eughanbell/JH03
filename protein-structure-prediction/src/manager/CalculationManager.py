from Calculation import Calculation

from enum import Enum
from io import StringIO
import json
import logging
import os
import time

ALPHAFOLD_PATH = "/home/ubuntu/alphafold"
MAX_CONCURRENT_CALCULATIONS = 1

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
        cls.calculations_list.append( Calculation(sequence=sequence, logger=main_logger) )

        cls.attempt_start_calculation() # Attempt to start this calculation process (will otherwise wait until available)
    
    @classmethod
    def cancel_calculation(cls, sequence: str):
        for idx, calculation in enumerate(cls.calculations_list):
            if calculation.sequence == sequence:
                if calculation.status == CalculationState.CALCULATING:
                    calculation.stop()
                calculation.cleanup()
                main_logger.info(f"Removing enqueued protein calculation for protein sequence: '{sequence}'.")
                cls.calculations_list.pop(idx)
                cls.attempt_start_calculation() # Now calculation is terminated, attempt to start a new calculation process
                return
        err = f"Could not cancel protein sequence calculation: sequence not currently in queue. Sequence: '{sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})
    
    @classmethod
    def download_calculation_result(cls, search_sequence: str, download_options: str):
        for calculation in cls.calculations_list:
            if calculation.sequence == search_sequence:
                if calculation.status == CalculationState.COMPLETE:
                    return calculation.getResults(download_options)
                if calculation.status == CalculationState.FAILED:
                    return calculation.log
                else:
                    err = f"Cannot download result: calculation is still in the {calculation.status} state."
                    main_logger.warning(err)
                    return json.dumps({"detail":err})
        err = f"Cannot download result: not currently processing protein sequence'{search_sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})
    
    @classmethod
    def attempt_start_calculation(cls):
        if cls.concurrent_calculations_count < MAX_CONCURRENT_CALCULATIONS:
            for calculation in cls.calculations_list:
                if calculation.status == CalculationState.WAITING:
                    calculation.start(callback = cls.attempt_start_calculation) # Once the calculation is complete, it should as a callback attempt  to start another calculation, now a space is free
                    return

    @classmethod
    def concurrent_calculations_count(cls):
        count = 0
        for calculation in cls.calculations_list:
            if calculation.is_alive():
                count += 1
        return count

class CalculationState(Enum):
    WAITING = 0
    CALCULATING = 1
    COMPLETE = 2
    FAILED = 3

    def __str__(self):
        return self.name