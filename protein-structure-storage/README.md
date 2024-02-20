# Protein Structure Storage 

## Internal Architectue

The overall goal of this container is to fetch from uniprot a list of all
the databases with information about a certain protein. It selects all
of the sources that we support (and the user selects). It scores them based on 
their properties, and picks the best scoring one. 
The selected protein is sent to the cache, so next time we can return it
immediately without checking uniprot. Finally it is returned to the user.

Uniprot stores many sources of information for a given protein.
By default we look at structure files (given by `pdb` and `alphafold` databases).
But Uniprot also stores sources for nucleotide/protein sequences,
go annotations, family/domain, etc.

By creating a new database entry classes, one can extend the code to work with those
different sources of information that uniprot supports.


## Learning by Example: A Walkthough to Support Sequence files

To find out how this system works, we imagine that you want the system to support Sequence files instead of structure files.

The steps we need to follow are:

1. Check which databases uniprot links to for sequences
2. Find out how we can fetch sequence files from these databases
3. Write a file in `src/database_entries/` for each database to score and fetch the files
4. Reference it in `src/uniprot.py`


### Which databases to support

We inspect a protein as an exmple [P06213](https://www.uniprot.org/uniprotkb/P06213/entry).
Our parser takes in an xml file from uniprot that stores all of the
relevant information about a protein.

Take a look at the file [P06213.xml](https://rest.uniprot.org/uniprotkb/P06213.xml).
In the xml dom, external databases are at `<uniprot><entry><dbReference>...`, 
here are some examples of `dbReference` objects from the linked file.

```xml
<dbReference type="EMBL" id="M27195">
	<property type="protein sequence ID" value="AAA86791.1"/>
	<property type="status" value="JOINED"/>
	<property type="molecule type" value="Genomic_DNA"/>
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
```

Each `dbReference` node is an entry in an external database, 
and will be referring to different file types depending on what type of information 
the database stores.

When a protein is requested, and it isn't in the cache, `src/pss.py` will 
ask for a list of potential databases.
`src/uniprot.py` iterates over all of the `dbReference` nodes,
creating `ExternalDatabaseEntry` objects (when the db is supported).
It returns that list to `src/pss.py`.

Protein Structures are `pdb` files, this is what we support by default,
and the sources are `PDB` (there are a few databases, ie PDBe, RSCB)
or `AlphafoldDB`, which give
