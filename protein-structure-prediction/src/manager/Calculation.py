from .CalculationState import CalculationState
from .settings import DownloadOptions, ALPHAFOLD_PATH

from io import StringIO
import json
import os
import re
import shlex
import subprocess
import time
import threading
import zipfile

TERMINATION_TIMEOUT = 5 # How long Calculation.stop() should wait before assuming termination has failed and attempts to kill thread.

class Calculation(threading.Thread):
    def __init__(self, sequence: str, logger):
        self.sequence = sequence
        self.logger = logger
        self.status = CalculationState.WAITING
        self.waiting_since = time.time()
        self.start_time = None
        self.on_complete_callback = lambda:None # Function to call when calculation complete

        self.process = None
        self.process_exit_code = None
        self.log = open(f"{ALPHAFOLD_PATH}/_{id(self)}.log", "a")
        
        self.output_directory = f"{ALPHAFOLD_PATH}/_{id(self)}"
        os.mkdir(self.output_directory)

        super().__init__()
    
    def run(self):
        self.status = CalculationState.CALCULATING

        # Create fasta sequence file
        with open(f"{ALPHAFOLD_PATH}/_{id(self)}.fasta", "w") as f:
            f.write(f">Temporary sequence file for {id(self)}|\n{self.sequence}")

        # Create command
        command = f"""python3
            {ALPHAFOLD_PATH}/docker/run_docker.py
            -v {ALPHAFOLD_PATH}:{ALPHAFOLD_PATH}
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
            shlex.split(f"mamba run -n alphafold --no-capture-output {command}"),
            stdout = self.log,
            stderr = self.log
        )

        # Wait for completion
        self.process_exit_code = self.process.wait()

        # Complete
        if self.process_exit_code == 0:
            self.status = CalculationState.COMPLETE
        else:
            self.status = CalculationState.FAILED

        self.on_complete_callback()
    
    def stop(self):
        self.status = CalculationState.FAILED
        # Attempt termination of process (run will end thread once process terminated)
        self.process.terminate()
        self.join(TERMINATION_TIMEOUT)
        if not self.is_alive():
            return
        # Termination of process failed, attempt kill (run will end thread once process killed)
        self.process.kill()
        self.join(TERMINATION_TIMEOUT)
        if not self.is_alive():
            return
        # Process kill failed, attempt to stop thread directly
        self._stop_event.set()

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
            err = f"No files match specified type '{download_type}'. Valid download requests are: '{','.join(DownloadOptions.keys())}'"
            self.logger.warning(err)
            result = json.dumps({"detail":err})
        elif len(result_filenames) == 1: # One file selected, return as is
            with open(f"{self.output_directory}/{result_filenames[0]}") as f:
                result = f.read()
        else: # Multiple files selected, zip and return zipfile
            result = StringIO.StringIO()
            with zipfile.ZipFile(result, "w") as zip_file: # Open result buffer
                for filename in result_filenames:
                    zip_file.write(f"{self.output_directory}/{filename}", filename)
            result = result.getvalue()
        
        return result

    def cleanup(self):
        """ Remove all files associated with this file from filesystem. """
        if self.is_alive():
            return False # Do not attempt to clean up if thread still running!
        
        self.log.close()
        os.remove(f"{ALPHAFOLD_PATH}/_{id(self)}.log")
        os.remove(f"{ALPHAFOLD_PATH}/_{id(self)}.fasta")
        os.rmdir(self.output_directory)
    
    def set_on_complete_callback(self, callback_fn):
        self.on_complete_callback = callback_fn

    def __str__(self):
        return json.dumps({
            "sequence": self.sequence,
            "calculation_state": str(self.status),
            "waiting_since_timestamp": self.waiting_since,
            "calculation_start_timestamp": self.start_time,
        })