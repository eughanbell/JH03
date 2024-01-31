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


class Calculations:
    @classmethod
    def list_calculations(cls):
        return json.dumps(cls.calculations_list)

    @classmethod
    def add_calculation(cls, sequence: str):
        cls.calculations_list.append( Calculations(sequence=sequence) )
    
    @classmethod
    def download_calculation_result(cls, search_sequence: str):
        for elem in cls.calculations_list:
            if elem.sequence == search_sequence:
                if elem.status == CalculationState.COMPLETE:
                    return elem.result
                else:
                    err = f"Cannot download calculation that is still in the {elem.status} state."
                    logger.error(err)
                    return err

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
    
    def __repr__(self):
        return {
            "sequence": self.sequence,
            "calculation_state": str(self.status),
            "waiting_since_timestamp": self.waiting_since,
            "calculation_start_timestamp": self.start_time,
        }