from CalculationManager import CalculationState, ALPHAFOLD_PATH
from DownloadOptions import DownloadOptions

from io import StringIO
import json
import os
import re
import subprocess
import time
import threading
import zipfile

class Calculation(threading.Thread):
    def __init__(self, sequence: str, logger):
        self.sequence = sequence
        self.logger = logger
        self.status = CalculationState.WAITING
        self.waiting_since = time.time()
        self.start_time = None

        self.process = None
        self.log = open(f"{ALPHAFOLD_PATH}/_{id(self)}.log", "a")
        
        self.output_directory = f"{ALPHAFOLD_PATH}/_{id(self)}"
        os.mkdir(self.output_directory)
    
    def run(self):
        # Create fasta sequence file
        with open(f"{ALPHAFOLD_PATH}/_{id(self)}.fasta", "w") as f:
            f.write(f">Temporary sequence file for {id(self)}|\n{self.sequence}")

        # Create command
        command = f"""python3
            {ALPHAFOLD_PATH}/docker/run_docker.py
            --fasta_paths={ALPHAFOLD_PATH}/_{id(self)}.fasta
            --max_template_date=9999-12-31
            --data_dir=/mnt/data/
            --use_gpu=false"
            --output_dir={ALPHAFOLD_PATH}/_tmp
        """

        # Set calculation start timestamp
        self.start_time = time.time()

        # Begin execution
        self.process = subprocess.Popen(
            f"mamba run -n alphafold --no-capture-output {command}",
            shell = True, 
            stdout = self.log,
            stderr = self.log
        )

        return self.process.wait()

    def get_logs(self):
        logs = ""
        with open(f"{ALPHAFOLD_PATH}/_{id(self)}.log") as f:
            logs = f.read()
        return logs
    
    def get_results(self, download_type):
        if self.status != CalculationState.COMPLETE:
            return False

        # Select files to return
        download_type_pattern = DownloadOptions.get(download_type, "$.") # If type not found, use pattern that will never match (e.g., return no files)
        result_filenames = [filename for filename in os.listdir(self.output_directory) if re.match(download_type_pattern, filename)]
        self.logger.info(f"Preparing files for download: {','.join(result_filenames)}.")

        # Return files
        result = ""
        if len(result_filenames) == 0: # No files selected, return error
            err = f"No files match specified type '{download_type}'. Valid download requests are: '{','.join(DownloadTypes.keys())}'"
            self.logger.warning(err)
            result = json.dumps({"detail":err})
        elif len(result_filenames) == 1: # One file selected, return as is
            with open(f"{self.output_directory}/{result_filenames[0]}") as f:
                result = f.read()
        else: # Multiple files selected, zip and return zipfile
            result = StringIO.StringIO()
            with zipfile.ZipFile(result, "w") as zf:
                for filename in result_filenames:
                    zf.write(f"{self.output_directory}/{filename}", filename)
        
        return result

    def __str__(self):
        return json.dumps({
            "sequence": self.sequence,
            "calculation_state": str(self.status),
            "waiting_since_timestamp": self.waiting_since,
            "calculation_start_timestamp": self.start_time,
        })