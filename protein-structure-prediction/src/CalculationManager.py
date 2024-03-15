from .Calculation import Calculation
from .CalculationState import CalculationState
from settings import MAX_CONCURRENT_CALCULATIONS

import json
import logging
import sys

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.DEBUG)
main_logger.addHandler(log_handler)

class CalculationManager:

    calculations_list = []

    @classmethod
    def list_calculations(cls):
        main_logger.info("Serving calculations list.")
        return f"[{','.join([str(elem) for elem in cls.calculations_list])}]"

    @classmethod
    def add_calculation(cls, sequence: str):
        for calculation in cls.calculations_list:
            if calculation.sequence == sequence:
                err = f"Cannot enqueue calculation: protein sequence already in calculations list. Sequence: '{sequence}'."
                main_logger.warning(err)
                return json.dumps({"detail":err})
        
        main_logger.info(f"Enqueing calculation for protein sequence: '{sequence}'.")
        cls.calculations_list.append( Calculation(sequence=sequence, logger=main_logger) )

        cls.attempt_start_calculation() # Attempt to start this calculation process (will otherwise wait until available)
    
    @classmethod
    def cancel_calculation(cls, sequence: str):
        for idx, calculation in enumerate(cls.calculations_list):
            if calculation.sequence == sequence:
                main_logger.info(f"Stopping and removing enqueued protein calculation for protein sequence: '{sequence}'.")
                if calculation.status == CalculationState.CALCULATING:
                    calculation.stop()
                calculation.cleanup()
                cls.calculations_list.pop(idx)
                cls.attempt_start_calculation() # Now calculation is terminated, attempt to start a new calculation process
                return
        err = f"Could not cancel protein sequence calculation: sequence not currently in queue. Sequence: '{sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})

    @classmethod
    def get_calculation_logs(cls, sequence: str):
        for idx, calculation in enumerate(cls.calculations_list):
            if calculation.sequence == sequence:
                return calculation.get_logs()
        err = f"Cannot return logs: no calculation exists for sequence '{sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})
    
    @classmethod
    def download_calculation_result(cls, search_sequence: str, download_options: str):
        for calculation in cls.calculations_list:
            if calculation.sequence == search_sequence:
                if calculation.status == CalculationState.COMPLETE:
                    return calculation.get_results(download_options)
                if calculation.status == CalculationState.FAILED:
                    return calculation.get_logs()
                else:
                    err = f"Cannot download result: calculation is still in the {calculation.status} state."
                    main_logger.warning(err)
                    return json.dumps({"detail":err})
        err = f"Cannot download result: not currently processing protein sequence'{search_sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})

    @classmethod
    def attempt_start_calculation(cls):
        if cls.concurrent_calculations_count() < MAX_CONCURRENT_CALCULATIONS:
            main_logger.info("Attempting to start new calculation.")
            for calculation in cls.calculations_list:
                if calculation.status == CalculationState.WAITING:
                    main_logger.info(f"Starting calculation for protein sequence: '{calculation.sequence}'.")
                    calculation.set_on_complete_callback(cls.attempt_start_calculation)
                    calculation.start() # Once the calculation is complete, it should as a callback attempt  to start another calculation, now a space is free
                    return
            main_logger.info("Cannot start new calculation at this time: no waiting calculations to start.")
        else:
            main_logger.info(f"Cannot start new calculation at this time: maximum concurrent calculations threshold {MAX_CONCURRENT_CALCULATIONS} reached.")

    @classmethod
    def concurrent_calculations_count(cls):
        """ Count all alive calculation processes """
        count = 0
        for calculation in cls.calculations_list:
            if calculation.is_alive():
                count += 1
        return count