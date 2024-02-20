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


## Learning by Example: A Walkthough to Support EMBL Sequence files

We will use [P06213](https://www.uniprot.org/uniprotkb/P06213/entry).
Our parser takes in an xml file from uniprot that stores all of the
relevant information about a protein.

Take a look at the file [P06213.xml](https://rest.uniprot.org/uniprotkb/P06213.xml).
In the xml dom, db entries are at `uniprot->entry->dbReference`, here are some examples
of `dbReference` objects from the linked file.

```xml
<dbReference type="EMBL" id="M27195">
	<property type="protein sequence ID" value="AAA86791.1"/>
	<property type="status" value="JOINED"/>
	<property type="molecule type" value="Genomic_DNA"/>
</dbReference>
<dbReference type="CCDS" id="CCDS12176.1">
	<molecule id="P06213-1"/>
</dbReference>
<dbReference type="PIR" id="A37348">
	<property type="entry name" value="INHUR"/>
</dbReference>
<dbReference type="RefSeq" id="NP_001073285.1">
	<molecule id="P06213-2"/>
	<property type="nucleotide sequence ID" value="NM_001079817.2"/>
</dbReference>
<dbReference type="PDB" id="1GAG">
	<property type="method" value="X-ray"/>
	<property type="resolution" value="2.70 A"/>
	<property type="chains" value="A=1005-1310"/>
</dbReference>
<dbReference type="AlphaFoldDB" id="P06213"/>
```

Each `dbReference` is an entry in an external database, 
and will be pointing to different files depending on what the database is for.

Our uniprot parser will iterate over all of the `dbReference` objects,
and select the ones that are supported.

Protein Structures are `pdb` files, this is what we support by default,
and the sources are `PDB` (there are a few databases, ie PDBe, RSCB) 
or `AlphafoldDB`, which give
