for i in $(seq 10 $1)
do
    rand_str=$(printf "p%05d" $((RANDOM % 100000)))

    curl 0.0.0.0:8000/retrieve_by_uniprot_id/${rand_str}?alphafold_only=True > ${rand_str}.pdb
    if [ ! -s ${rand_str}.pdb ] ; then
        rm ${rand_str}.pdb
    fi 
done
