# Protein Database Requests And Cache 

## Quickstart with single docker compose file

copy the compose file from `compose_only/compose.yaml` into your files and run 
```docker compose up```
which should automatically start the webapp.

You can now access the webapp and check the docs by going to
`0.0.0.0:8000/docs`. If this doesn't work, try `127.0.0.1:8000/docs`

## Usage

Protein files can be requested using uniprot ids. Any requested proteins
will be cached locally.

### Example Usage

```
curl 'http://0.0.0.0:8000/retrieve_by_uniprot_id/p02070'
```

see `example_scripts/` for more usage examples.

### Accessing MongoDB express web service
To inspect the cache database manually, if the containers are running, go to
`0.0.0.0:8081` or `127.0.0.1:8081`.
You will need to login, the credentials are 
```
username: admin
password: pass
```

The cache database will only be present if at least one pdb file has been requested.

## Building Docker Containers Locally

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

## Testing
`protein-structure-storage` unittests can be run by executing `python -m unittest` in the `protein-structure-storage/` folder.

## Pushing Built Containers to Docker Hub

TODO: push containers from shared account
at the moment only works for one person


```
docker build -t noamzeise/protein-structure-storage:latest protein-structure-storagbe
docker image push noamzeise/protein-structure-storage:latest
docker build -t noamzeise/protein-cache:latest protein-cache
docker image push noamzeise/protein-cache:latest
```
