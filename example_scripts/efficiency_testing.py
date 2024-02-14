import subprocess
from subprocess import call
import time
import sys
import glob


def repeatedScript(script, n=99):
    subprocess.call('rm *.pdb', shell=True)

    start=time.time()
    subprocess.call(f"./{script}.sh {n}",shell=True)
    end=time.time()
    change=len(glob.glob("*.pdb"))

    print(f"took {end-start} seconds to complete testing, where {change} PDB files were returned, each successful API call took on average {(end-start)/n} seconds")
    return 

def manualScript(script,vals=[]):
    #pass theoretical list of working sequences. 
    subprocess.call('rm *.pdb', shell=True)

    if vals==[]:
        vals=["p20303","p20103","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
    start=time.time()
    for val in vals:
        subprocess.call(f"./{script}.sh {val}", shell=True)
    end = time.time()   
    change=len(glob.glob("*.pdb"))

    print(f"took {end-start} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(end-start)/len(vals)} seconds")
    return 


if __name__ == "__main__":
    repeated_calls={"af_random":"download_alphafold_random","af":"download_alphafold","uniprot_random_cache":"download_cache_random","uniprot_random":"download_pdb_random","uniprot_cache":"download_cache","uniprot":"download_pdbs","upload":"upload_pdb"}
    manual_calls={"key_uniprot":"download_key_uniprot","key":"download_key","sequence":"download_sequence"}
    if len(sys.argv)==1:
        print("Please select an endpoint to test!")
    else:
        eps=sys.argv[1:]
        for ep in eps:
            if ep in repeated_calls.keys():
                repeatedScript(repeated_calls[ep])
            elif ep in manual_calls.keys():
                manualScript(manual_calls[ep])
