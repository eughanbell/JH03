# Protein Structure Storage - Internal Architecture

The overall goal of this container is to fetch
the best protein file that we can find from [uniprot](https://www.uniprot.org/).
We select all of the files resident in the source databases that we support 
(and that the user selects). 
They are scored based on their properties, and the best one is picked. 
The selected protein file is saved in the cache, so it is returned without checking uniprot the next time it is requested. 
Finally, it is returned to the user.

Uniprot stores many sources of information for a given protein.
By default we look at structure files (given by _pdb_ and _alphafold_ databases), but uniprot also stores sources for nucleotide/protein sequences,
go annotations, family/domain, etc.

By creating new database entry classes, an individual can extend the code to work with all the
different sources of information that uniprot supports. This is illustrated below.




# Learning by Example: A Walkthrough for Supporting Sequence Files

To find out more about the system architecture, we imagine that you want to return protein sequence files instead of the structure files currently returned.

The steps we need to follow are:

1. Check which databases uniprot references for sequence files
2. Find out how we can fetch the sequence files from these databases
3. Write a class in `src/database_entries/` for each database
4. Reference it in `src/uniprot.py`



## 1. Which databases to support

We use a protein as an example [P06213](https://www.uniprot.org/uniprotkb/P06213/entry).

Take a look at the file from uniprot covering this protein:
[P06213.xml](https://rest.uniprot.org/uniprotkb/P06213.xml).
In the xml DOM (the tree of nodes that make up the file),
external databases are under `<uniprot><entry>` with tag _dbReference_.
Here are some examples of _dbReference_ nodes from the linked file.

```xml
<uniprot ...>
	...
	<entry ...>
		...
		<dbReference type="EMBL" id="M10051">
			<property type="protein sequence ID" value="AAA59174.1"/>
			<property type="molecule type" value="mRNA"/>
		</dbReference>
		<dbReference type="CCDS" id="CCDS12176.1">
			<molecule id="P06213-1"/>
		</dbReference>
		<dbReference type="PDB" id="1GAG">
			<property type="method" value="X-ray"/>
			<property type="resolution" value="2.70 A"/>
			<property type="chains" value="A=1005-1310"/>
		</dbReference>
		<dbReference type="AlphaFoldDB" id="P06213"/>
		...
	</entry>
	...
</uniprot>
```

Each _dbReference_ node is an entry in an external database, 
and will be referring to different file types depending on what kind of information 
the database stores.

When a protein is requested by the user (handled in `src/main.py`), and it isn't in the cache, 
`src/pss.py` will request a list of potential databases from `src/uniprot.py`.
This code iterates over all of the _dbReference_ nodes from uniprot,
creating `ExternalDatabaseEntry` objects when the db is supported.
It returns that list to `pss.py`.

A database is supported if it is listed in `EXTERNAL_DATABASES` within `uniprot.py`,
and it is requested by the user (when the user specifies which dbs to check). 

We check the _dbReference_ nodes, and see that sequence databases include _EMBL_, _CCDS_, etc.
From these, we will add _EMBL_ to our list of supported databases, as most proteins have this  listed.



# 2. Fetching files from _EMBL_

We visit the website of _EMBL_, and enter the id
in the first _dbReference_ node in the xml file (`M10051`). 
Using that gets us to this [page](https://www.ebi.ac.uk/ena/browser/view/M10051).

We want the _EMBL_ file, so right click the _download EMBL_ button and press copy link.
Giving us the following url.

```
https://www.ebi.ac.uk/ena/browser/api/embl/M10051?download=true
```

Strip the `?download=true` ending and put it into our browser, which gives us [the file
in plaintext](https://www.ebi.ac.uk/ena/browser/api/embl/M10051.1), exactly what we want.

Now we can retrieve any _EMBL_ file found in uniprot by taking the
id and adding it to the url like so.

```
https://www.ebi.ac.uk/ena/browser/api/embl/{EMBL_ID}
```

Now we have everything we need to write code for _EMBL_.



## 3. Writing a database entry class for _EMBL_

First make a new file `src/database_entries/embl_entry.py`. 

We need to subclass `ExternalDatabaseEntry`, so import it by adding the following line.

```python
from .abstract_entry import ExternalDatabaseEntry
```

`ExternalDatabaseEntry` is an abstract class with two methods we need to override,
so at minimum we require the following.

```python
class EMBLEntry(ExternalDatabaseEntry):

	def fetch(self):
		return ""

	def calculate_raw_quality_score(self):
		return 0
```

We now need to fill in the details of these two blank functions.

First fetch needs to return the _EMBL_ file using the url we discovered in section 2.
To do this we need to be able to get a text file from a url. To help with this we add another import.
```python
from ..helpers import get_from_url
```

Now it is trivial to write a fetch function.

```python
def fetch(self):
	embl_id = self.entry_data["id"]
	embl_url = f"https://www.ebi.ac.uk/ena/browser/api/embl/{embl_id}"
	return get_from_url(embl_url).decode() # decode bytes into string
```

One question you may have is how is `self.entry_data` laid out?
All the details of a _dbReference_ is stored within, plus some extra metadata.

So given the entry from _EMBL_ 
```xml
<dbReference type="EMBL" id="M10051">
	<property type="protein sequence ID" value="AAA59174.1"/>
	<property type="molecule type" value="mRNA"/>
</dbReference>
```
We obtain
```python
entry_data = {
	'external_db_name': "EMBL",
	'id': "M10051"
	# properties
	'protein sequence ID': "AAA59174.1",
	'molecule type': "mRNA",
	# metadata
	'protein_metadata': {
		'sequence': "MATGGRRGA...",
		# etc...
	}
}
```

Now armed with this knowledge we can write a scoring function.

```python
def calculate_raw_quality_score(self):
	score = 0
	molecule_type = self.entry_data["molecule type"]
	if molecule_type == "mRNA":
		score = 0.4
	elif molecule_type == "Genomic DNA":
		score = 0.2
	else
		score = 0.1
	return score
```	

## 4. Add to external databases

Finally we add our new database entry object to `src/uniprot.py`.

```python
# ...
from .database_entries import embl_entry
# ...
EMBL_DB_NAME = "EMBL"
EXTERNAL_DATABASES = {
    EMBL_DB_NAME: embl_entry.EMBLEntry,
}
```

Now when you run the project, and go to `localhost:8000/retrieve_by_uniprot_id/P06213`,
you will get an `EMBL` file returned to you.


## Extra: Using a yaml File for Scoring Weights

Lets say we want to customise our scoring function by specifying values in a yaml file
in a docker volume (can be changes without rebuilding containers). 
First we import the weight importer function and specify a dictionary of modifiable weights.
We override this with a file called `embl_weights.yaml` that the user can put in a `config/`
directory when docker composing the project.

```python
from .weight_importer import import_weights

embl_weights  = {
    'types': {
        'default': 0.1,
        'Genomic DNA': 0.2,
        'mRNA': 0.4,
    },
}
embl_weights = import_weights(embl_weights, "/src/config/embl_weights.yaml")
```

Now we can update the `calculate_score` function to use this dictionary. 
We use the default type score when we don't recognise the molecule type.

```python
def calculate_raw_quality_score(self):
	molecule_type = self.entry_data["molecule type"]
	score = embl_weights['types'].get(molecule_type, embl_weights['types']['default'])
	return score
```

Now we can put a file called `embl_weights.yaml` in a `config/` folder that is beside the docker compose. To override the python dict it would need a structure like the following.

```yaml
types:
  mRNA: 0.8
  default: 0
```

It will override the dictionary with these values, allowing the user to customise the scoring function without building the containers.


Now we have an externally customisable entry class for the _EMBL_ database.
The next step would be to write similar entries for other sequence databases that uniprot may return.
