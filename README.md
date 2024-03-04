# Protein Database Requests And Cache 

Fetch protein structure files in the pdb format using a uniprot id.
Any requested proteins will be cached for quicker retrieval if requested again.

# Quickstart

You will need docker compose.

Save the file `compose_only/compose.yaml` into your files as `compose.yaml` and run 
```docker compose up```
in the same folder.

You can now access the webapp and check the docs by going to
`127.0.0.1:8000/docs`.

# Usage

## Protein Structure Storage

* Get by uniprot ID
```
curl 'http://0.0.0.0:8000/retrieve_by_uniprot_id/p02070'
```

* Upload file and get database key as response
```
curl -w "\n" -X POST -F file=@path/to/my/file.pdb 0.0.0.0:8000/upload_pdb/
```

* see `example_scripts/` for more usage examples.

### Changing Scoring Weights

The container picks which structure to return based on it's properties.

The weights used to score proteins can be changed by the user without rebuilding containers.
See the `config` folder README for details. 

In brief, adding a folder called `config` next to `compose.yaml`, one can put yaml files into
this folder and they will change the weights when the containers are run with docker compose.

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

# Inspecting the Cache

Ensure the containers are running, go to `127.0.0.1:8082` 
in your browser.
You will need to login, the credentials are 
```
username: admin
password: pass
```

The cache database will only be present if at least one pdb file has been requested.


# Running on Kubernetes

See the `kubernetes` folder README for info on running on kubernetes



# Development

## Building Locally

### With Docker Compose

If you have `docker` and `docker compose` installed you can do
```
git clone https://github.com/eughanbell/JH03.git
cd JH03
docker compose up
```

When you edit the code, you will need to run the following first to see your changes reflected
```
docker compose build
```

### Without Docker Compose

#### Protein Structure Storage

make sure you are in this project's root folder

* build the docker image
```
docker build -t pss protein-structure-storage
```
* run the docker image
```
docker run --publish 8000:5000 pss
```

#### Protein Cache
	
build in similar way to pss, but make sure pss is still running.
```
docker build -t pc protein-cache
```
to run, we will map to 7000 instead of 8000 to not conflict with pss.
```
docker run --publish 7000:6000 pc
```

# Testing

There are tests for `pss` and `psp`. To run, navigate to the `protein-structure-storage` or 
`protein-structure-prediction` folders. Make sure you have the nessecary python libraries installed (by running `pip install -r requirements.txt`).
```python
python -m unittest
```

# Performance Testing

The performance of the API requests can be tested with either provided or arbitrary data

- Testing Provided Data

Navigate to ./performance_testing, execute:
```
performance_testing.py {choice of API Request} {file}
```
Refer to manuals.json keys for a list of currently available testing methods. An example file is provided to demonstrate the required data arrangement.

- Testing Arbitrary Data

Multiple sequential and random Uniprot IDs can be tested in succession, the choice of exclusively testing alphafold is available. Execute as such:
```
performance_testing.py {API Request 1} {Api Request 2} ... {Api Request N}
```
Refer to increments.json & randoms.json keys for a list of currently available testing methods.


# Pushing Built Containers to Docker Hub

This is done automaically by a gitlab or github pipeline.

```
docker build -t noamzeise/protein-structure-storage:latest protein-structure-storage
docker image push noamzeise/protein-structure-storage:latest
docker build -t noamzeise/protein-cache:latest protein-cache
docker image push noamzeise/protein-cache:latest
```
