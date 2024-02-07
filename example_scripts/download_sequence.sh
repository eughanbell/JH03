#/!bin/bash
curl 0.0.0.0:8000/retrieve_by_sequence/$1 > $1.pdb
if [ ! -s $1.pdb ] ; then
    rm $1.pdb
fi 

