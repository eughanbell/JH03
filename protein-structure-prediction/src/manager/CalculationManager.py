from enum import Enum
import json
import logging
import time

logger = logging.getLogger(__name__)

class CalculationState(Enum):
    WAITING = 0
    CALCULATING = 1
    COMPLETE = 2
    FAILED = 3

    def __str__(self):
        return self.name


class CalculationManager:

    calculations_list = []

    @classmethod
    def list_calculations(cls):
        return f"[{','.join([str(elem) for elem in cls.calculations_list])}]"

    @classmethod
    def add_calculation(cls, sequence: str):
        for calculation in cls.calculations_list:
            if calculation["sequence"] == sequence:
                err = f"Cannot enqueue calculation: protein sequence already in calculations list. Sequence: '{sequence}'."
                logger.warning(err)
                return json.dumps({"detail":err})
        cls.calculations_list.append( CalculationManager(sequence=sequence) )
    
    @classmethod
    def remove_calculation(cls, sequence: str):
        for idx, calculation in enumerate(cls.calculations_list):
            if calculation["sequence"] == sequence:
                if calculation["status"] == CalculationState.CALCULATING:
                    logger.warning("CODE FOR KILLING ONGOING CALCULATION NONEXISTENT!")
                logger.info(f"Removing enqueued protein calculation for protein sequence: '{sequence}'.")
                cls.calculations_list.pop(idx)
                return
        err = f"Could not remove protein sequence: sequence not currently in queue. Sequence: '{sequence}'."
        logger.warning(err)
        return json.dumps({"detail":err})
    
    @classmethod
    def download_calculation_result(cls, search_sequence: str):
        for elem in cls.calculations_list:
            if elem.sequence == search_sequence:
                if elem.status == CalculationState.COMPLETE:
                    return elem.result
                else:
                    err = f"Cannot download result: calculation is still in the {elem.status} state."
                    logger.warning(err)
                    return json.dumps({"detail":err})
        err = f"Cannot download result: not currently processing protein sequence'{search_sequence}'."
        logger.warning(err)
        return json.dumps({"detail":err})

    def __init__(self, sequence: str):
        self.sequence = sequence
        self.status = CalculationState.WAITING
        self.waiting_since = time.time()
        self.start_time = None
        self.result = None
    
    def begin_calculation(self):
        if self.status != CalculationState.WAITING:
            logger.error("Cannot start calculation for sequence not in WAITING state.")
            return 1
        self.start_time = time.time()
        # Actually begin PSP calculations
    
    def __str__(self):
        return json.dumps({
            "sequence": self.sequence,
            "calculation_state": str(self.status),
            "waiting_since_timestamp": self.waiting_since,
            "calculation_start_timestamp": self.start_time,
        })