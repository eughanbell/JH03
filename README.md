# Protein Database Requests And Cache 

Fetch protein structure files in the pdb format using a uniprot id.
Any requested proteins will be cached for quicker retrieval if requested again.

# Quickstart

You will need docker compose.

Save the file `compose_only/compose.yaml` into your files as `compose.yaml` and run 
```docker compose up``` in the same folder.

You can now use the project. Check the docs by going to
`127.0.0.1:8000/docs`.

# Example Usage

## Protein Structure Storage

* Get by uniprot ID
```
curl "http://0.0.0.0:8000/retrieve_by_uniprot_id/p02070"

# or get from a specific database

curl "http://0.0.0.0:8000/retrieve_by_uniprot_id/p02070?db=pdb"
```

* Upload file and get database key as response (the @ before the file is important)
```
curl -w "\n" -X POST -F file=@path/to/my/file.pdb "0.0.0.0:8000/upload_pdb/"

# Can customise the uploaded protein properties

curl -w "\n" -X POST -F file=@path/to/my/file.pdb "0.0.0.0:8000/upload_pdb/?db=mydb&score=0.4"
```

* see `example_scripts/` or the fastapi docs at `0.0.0.0:8000/docs` for more info/examples.

#### Changing Scoring Weights

Protein structures are selected based on their properties.

The weights used to score proteins can be changed by the user without rebuilding containers.
See the `config` folder README for details. 

In brief, adding a folder called `config` next to the `compose.yaml`file , 
one can put text files into this folder and they will change the weights 
when the containers are run with docker compose.

# Protein Structure Prediction
_This container is a prototype, and is likely unstable. Use with caution._

This service can be used to, given a raw protein sequence, use Google Deepmind's Alphafold algorithm to predict new strucutes. Multiple calculations can be enqueued concurrently, and their results downloaded upon completion.

## Setup
In `protein-structure-prediction/settings.py`, the following parameters can be specified:
`MAX_CONCURRENT_CALCULATIONS` - the maximum number of Alphafold calculations the calculation manager should attempt to run simultaneously. It is recommended to leave this set to 1.
`DownloadOptions` - RegEx patterns for matching different subsets of the files Alphafold outputs for download.

The port used is specified in `compose.yaml` and in `protein-structure-prediction/Dockerfile`.

Google Deepmind's Alphafold must be downloaded and built from [https://github.com/google-deepmind/alphafold](https://github.com/google-deepmind/alphafold) using the instructions provided there.

The following host machine mappings must be set in `compose.yaml`:
- `/path/to/alphafold/container/directory : /mnt/alphafold` - the path to the Alphafold container directory on the host machine, from where `{dir}/docker/run_docker.py` is called.
- `/path/to/alphafold/data/directory : /mnt/data` - the path to the required Alphafold databases on the host machine.
- `/tmp/alphafold : /tmp/alphafold` - the path to where temporary processing files and Alphafold output should be stored on the host machine.

## Example Usage
_In all the below cases, {protein-sequence} refers to a raw IUPAC format nucleotide sequence, not a .fasta file._

* Add new protein sequence to predict structure of. Will add to calculations queue.
```
curl 'http://0.0.0.0:7000/calculate_structure_from_sequence/{protein-sequence}'
```

* Remove a protein sequence from the calculations queue, terminating the AlphaFold calculation if the calculation is ongoing.
```
curl 'http://0.0.0.0:7000/cancel_calculation/{protein-sequence}'
```

* Get the logs of an ongoing or completed calculation from the calculations queue.
```
curl 'http://0.0.0.0:7000/get_calculation_logs/{protein-sequence}'
```

* List all calculations (pending, processing, complete and failed) in the calculations queue. Returns a JSON list of objects representing every calculation in the queue.
```
curl 'http://0.0.0.0:7000/list_calculations/'
```

Returned objects have the following attributes:
- sequence: *str*
- calculation_state: *str*
- waiting_since_timestamp: *float*
- calculation_start_timestamp: *float*

`calculation_state` can take the following values:
- PENDING: waiting to begin AlphaFold prediction calculation
- PROCESSING: an AlphaFold prediction calculation is currently ongoing for this protein
- COMPLETE: the AlphaFold prediction for this protein is complete, and the `.pdb` file ready to download.
- FAILED: the AlphaFold prediction for this protein failed, and the error message file is ready to download.

* Download the results of a completed prediction (giving protein sequence to identify the result file). Will return a raw file if one file requested, or will return a zipfile if multiple. By default returns all data. If calculation has failed, results will be returned instead.
```
curl 'http://0.0.0.0:7000/download/{protein-sequence}&download={args}'
```
`args` can take several different values, specified in `settings.py` including `all_data` and `ranked_pdb` to get just the best `.pdb` files.


# Performance Testing / Cache Warming

See the `performance_testing` folder README on instruction for testing api performance and warming the cache.

In brief, with the project running, navigate to the `performace_testing` folder and run
```
python performance_testing.py uniprot my_list_of_uniprot_ids.txt
```
This warms the cache with a text file containing a uniprot id on each line.


# Inspecting/Clearing the Cache

With the project running, go to `127.0.0.1:8082` 
in your browser.
You will need to login, the credentials are 
```
username: admin
password: pass
```

The cache database will only be present if at least one pdb file has been requested.


The cache will be persistent between container restarts. It can be cleared using the api with
the `/clear_cache/` pss endpoint.


# Building Locally

If you have `git`, `docker` and `docker compose` installed you can do
```
git clone https://github.com/eughanbell/JH03.git
cd JH03
docker compose up --build
```

# Testing

There are tests for `pss` and `psp`. To run, navigate to the `protein-structure-storage` or 
`protein-structure-prediction` folders. Make sure you have the necessary python libraries installed (by running `pip install -r requirements.txt`), then run the following.
```python
python -m unittest
```


# Running on Kubernetes

See the `kubernetes` folder README for info on running on kubernetes
