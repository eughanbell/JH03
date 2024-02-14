#/!bin/bash
curl 0.0.0.0:8000/retrieve_key_by_uniprot_id/$1 > $1.pdb
if [ ! -s $1.pdb ] ; then
    rm $1.pdb
fi 

