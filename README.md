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
docker run --publish 8000:5000 pss
```
you should see "Hello, World!" followed by some flask messages
* test the example endpoint by visiting `0.0.0.0:8000/retrieve_by_key/` in a browser. You should get some text with the id.


#### Docs

To see documentation on the available endpoints visit `0.0.0.0:8000/docs/` in a browser while the server is running.
