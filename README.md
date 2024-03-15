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

## Protein Structure Prediction

* Add new protein sequence to predict structure of. Will add to calculations queue.
```
curl 'http://0.0.0.0:7000/calculate_protein_structure_from_sequence/{protein-sequence}'
```

* List all calculations (pending, processing and complete) in the calculations queue.
```
curl 'http://0.0.0.0:7000/list_calculations/'
```

* Download the .pdb protein structure file from a completed prediction (giving protein sequence to identify the result file).
```
curl 'http://0.0.0.0:7000/download_structure/{protein-sequence}'
```


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
