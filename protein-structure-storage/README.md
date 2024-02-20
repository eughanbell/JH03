# Protein Structure Storage 

## Internal Architectue

The overall goal of this container is to fetch from [uniprot](https://www.uniprot.org/) 
the best protein file that we can retrieve.
We select all of the files resident in the source databases that we support 
(and that the user selects). 
They are scored based on their properties, and the best one is picked. 
The selected protein file is sent to the cache, so next time we can return it
immediately without checking uniprot. Finally it is returned to the user.

Uniprot stores many sources of information for a given protein.
By default we look at structure files (given by `pdb` and `alphafold` databases).
But Uniprot also stores sources for nucleotide/protein sequences,
go annotations, family/domain, etc.

By creating a new database entry classes, one can extend the code to work with all the
different sources of information that uniprot supports. This is illustrated below.


## Learning by Example: A Walkthough for Supporting Sequence files

To find out more about the system architecture, we imagine that you want to return protein sequence files instead of the structure files currently returned.

The steps we need to follow are:

1. Check which databases uniprot references for sequence files
2. Find out how we can fetch the sequence files from these databases
3. Write a file in `src/database_entries/` for each database that scores and fetches the files
4. Reference it in `src/uniprot.py`


### 1. Which databases to support

We use a protein as an example [P06213](https://www.uniprot.org/uniprotkb/P06213/entry).

Take a look at the file from uniprot covering this protein:
[P06213.xml](https://rest.uniprot.org/uniprotkb/P06213.xml).
In the xml DOM (the tree of nodes that make up the file),
external databases are under `<uniprot><entry>` with tag `dbReference`, 
here are some examples of `dbReference` objects from the linked file.

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

Each `dbReference` node is an entry in an external database, 
and will be referring to different file types depending on what kind of information 
the database stores.

When a protein is requested by the user (handled in `src/main.py`), and it isn't in the cache, 
`src/pss.py` will request a list of potential databases from `src/uniprot.py`.
This code iterates over all of the `dbReference` nodes from uniprot,
creating `ExternalDatabaseEntry` objects when the db is supported.
It returns that list to `pss.py`.

A database is supported if it is listed in `EXTERNAL_DATABASES` within `uniprot.py`,
and it is requested by the user (when the user specifies which dbs to check). 

We check the `dbReference` nodes, and see that sequence databases include `EMBL`, `CCDS`, etc.

We will decide to just add `EMBL` to our list of supported databases, as most proteins have this
database listed.

## 2. Fetching files from `EMBL`

We visit the website that we can access `EMBL` through, and put in the id we found
in the first `dbReference` node we saw in the xml file (`M10051`). 
Using that gets us to this [page](https://www.ebi.ac.uk/ena/browser/view/M10051).

We want the `EMBL` file, so we right click the `download EMBL` button and press copy link.
Giving us the following url:

```
https://www.ebi.ac.uk/ena/browser/api/embl/M10051?download=true
```

We strip the `?download=true` ending and put it into our browser, which gives us [the file
in plaintext](https://www.ebi.ac.uk/ena/browser/api/embl/M10051.1), exactly what we want.
So we can retrieve any `EMBL` file we find referenced in uniprot by taking the
id and putting it into the url like so:

```
https://www.ebi.ac.uk/ena/browser/api/embl/{EMBL_ID}
```

Now we have everything we need to write a database entry for `EMBL`.
