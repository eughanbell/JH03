from enum import Enum
from io import StringIO
import json
import logging
import os
import re
import StringIO
import subprocess
import time
import zipfile

ALPHAFOLD_PATH = "/home/ubuntu/alphafold"

main_logger = logging.getLogger(__name__)

class CalculationState(Enum):
    WAITING = 0
    CALCULATING = 1
    COMPLETE = 2
    FAILED = 3

    def __str__(self):
        return self.name

# Explanation of Alphafold outputs
# https://blog.biostrand.ai/explained-how-to-plot-the-prediction-quality-metrics-with-alphafold2

DownloadTypes = {
    # Download predicted structure files
    "ranked_pdb": "^ranked_\d+\.pdb$",
    "ranked_cif": "^ranked_\d+\.cif$",
    "unrelaxed_pdb": "^unrelaxed_model_\d+.*\.pdb$",
    "unrelaxed_cif": "^unrelaxed_model_\d+.*\.cif$",
    
    # Download single file with ordering and confidence of rankings
    "ranking_debug": "^ranking_debug\.json",

    # Download confidence model files
    "confidence_model": "^confidence_model_\d+.*\.json$",
    
    # Download structure model pkl files
    "model_pkl": "^result_model_\d+.*\.pkl$",

    # Download misc metadata single files
    "features": "^features\.pkl$",
    "msas": "^msas$",
    "timings": "^timings.json$",
    "relax_metrics": "^relax_metrics.json$",

    # Download all files
    "all_data": "^$",
}

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
    def download_calculation_result(cls, search_sequence: str, download_type: str):
        for elem in cls.calculations_list:
            if elem.sequence == search_sequence:
                if elem.status == CalculationState.COMPLETE:
                    # Select files to return
                    download_type_pattern = DownloadTypes.get(download_type, "$.") # If type not found, use pattern that will never match (e.g., return no files)
                    result_filenames = [filename for filename in os.listdir(elem.result_directory) if re.match(download_type_pattern, filename)]
                    main_logger.info(f"Preparing files for download: {','.join(result_filenames)}.")

                    # Return files
                    result = ""
                    if len(result_filenames) == 0: # No files selected, return error
                        err = f"No files match specified type '{download_type}'. Valid download requests are: '{','.join(DownloadTypes.keys())}'"
                        main_logger.warning(err)
                        result = json.dumps({"detail":err})
                    elif len(result_filenames) == 1: # One file selected, return as is
                        with open(f"{elem.result_directory}/{result_filenames[0]}") as f:
                            result = f.read()
                    else: # Multiple files selected, zip and return zipfile
                        result = StringIO.StringIO()
                        with zipfile.ZipFile(result, "w") as zf:
                            for filename in result_filenames:
                                zf.write(f"{elem.result_directory}/{filename}", filename)
                    
                    return result

                if elem.status == CalculationState.FAILED:
                    return elem.logs
                else:
                    err = f"Cannot download result: calculation is still in the {elem.status} state."
                    main_logger.warning(err)
                    return json.dumps({"detail":err})
        err = f"Cannot download result: not currently processing protein sequence'{search_sequence}'."
        main_logger.warning(err)
        return json.dumps({"detail":err})

    def __init__(self, sequence: str):
        self.sequence = sequence
        self.status = CalculationState.WAITING
        self.waiting_since = time.time()
        self.start_time = None

        self.process = None
        self.stdout = StringIO()
        self.stderr = StringIO()
    
    def begin_calculation(self):
        if self.status != CalculationState.WAITING:
            main_logger.error("Cannot start calculation for sequence not in WAITING state.")
            return 1
        self.start_time = time.time()

        command = f"""python3
            {ALPHAFOLD_PATH}/docker/run_docker.py
            --fasta_paths={ALPHAFOLD_PATH}/_{self.sequence}.fasta
            --max_template_date=9999-12-31
            --data_dir=/mnt/data/
            --use_gpu=false"
            --output_dir={ALPHAFOLD_PATH}/_tmp
        """

        self.process = subprocess.Popen(f"mamba run -n alphafold --no-capture-output {command}", shell=True, stdout = self.stdout, stderr = self.stderr)
    
    def __str__(self):
        return json.dumps({
            "sequence": self.sequence,
            "calculation_state": str(self.status),
            "waiting_since_timestamp": self.waiting_since,
            "calculation_start_timestamp": self.start_time,
        })