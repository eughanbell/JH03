for n in {1..2}
do
    for i in $(seq 10 $n)
    do
        curl 0.0.0.0:8000/retrieve_by_uniprot_id/p020$i > $i.pdb
        if [ ! -s $i.pdb ] ; then
            rm $i.pdb
        fi 
    done
done