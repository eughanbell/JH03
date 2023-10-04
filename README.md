# Protein Database 


## Docker Setup

* Install docker, to make sure you have installed it correctly run
```
docker --version
```
If you get a version number there are no issues

### Running protein structure storage

make sure you are in this project's root folder

* build the docker image
```
docker build -t pss protein-structure-storage
```
* run the docker image
```
docker run pss
```
