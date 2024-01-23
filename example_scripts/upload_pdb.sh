# assumes 10.pdb -> 20.pdb files in current dir
for i in $(seq 10 20);
do
    if [ -f $i.pdb ]; then
	printf "%s\n" $i.pdb >> dbids.txt
	curl -w "\n" -X POST -F file=@$i.pdb 0.0.0.0:8000/upload_pdb/ >> dbids.txt
    fi
done
