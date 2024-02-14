import subprocess
from subprocess import call
import time
import sys
import glob


def repeatedScript(script, n=99):
    subprocess.call('del *.pdb', shell=True)

    start=time.time()
    subprocess.call(f"./{script}.sh {n}",shell=True)
    end=time.time()
    change=len(glob.glob("*.pdb"))

    print(f"took {end-start} seconds to complete testing, where {change} PDB files were returned, each successful API call took on average {(start-end)/n} seconds")
    return 

def manualScript(script,vals=[]):
    #pass theoretical list of working sequences. 
    subprocess.call('del *.pdb', shell=True)

    if vals==[]:
        vals=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
    start=time.time()
    for val in vals:
        subprocess.call(f"./{script}.sh {val}", shell=True)
    end = time.time()   
    change=len(glob.glob("*.pdb"))

    print(f"took {end-start} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/len(sequences)} seconds")
    return 


# def uniprotSimpleDownloadTime(n=99):
#     #n = no of curl requests to make, must be greater than 10
#     subprocess.call('del *.pdb', shell=True)

#     start=time.time()
#     subprocess.call(f"./download_pdbs.sh {n}",shell=True)
#     end=time.time()
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each successful API call took on average {(start-end)/n} seconds")
#     return 

# def uniprotSimpleDownloadCacheTime(n=99):
#     #n = no of curl requests to make, must be greater than 10    
#     subprocess.call('del *.pdb', shell=True)

#     start=time.time()
#     subprocess.call(f"./download_cache.sh {n}", shell=True)
#     end=time.time()
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/n} seconds")
#     return 

# def pdbUploadTime():

#     start=time.time()
#     subprocess.call("./upload_pdb.sh", shell=True)
#     end=time.time()
#     print(f"took {start-end} seconds to complete testing")

#     return 

# def uniprotRandomDownloadTime(n=99):
#     #n = no of curl requests to make, must be greater than 10
#     subprocess.call('del *.pdb', shell=True)

#     start=time.time()
#     subprocess.call(f"./download_pdbs_random.sh {n}",shell=True)
#     end=time.time()
#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/n} seconds")
#     change=len(glob.glob(".pdb"))


#     return 

# def uniprotRandomDownloadCacheTime(n=99):
#     #n = no of curl requests to make, must be greater than 10
#     subprocess.call('del *.pdb', shell=True)

#     start=time.time()
#     subprocess.call(f"./download_cache_random.sh {n}",shell=True)
#     end=time.time()
#     change=len(glob.glob(".pdb"))
#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/n} seconds")

#     return 

# #these are for WIP endpoints
# def sequenceDownloadTime(sequences=[]):
#     #pass theoretical list of working sequences. 
#     subprocess.call('del *.pdb', shell=True)

#     if sequences==[]:
#         sequences=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
#     start=time.time()
#     for sequence in sequences:
#         subprocess.call(f"./download_sequence.sh {sequence}", shell=True)
#     end = time.time()   
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/len(sequences)} seconds")
#     return 

# def keyDownloadTime(keys=[]):
#     #i have no idea what a key looks like so it will be the same as the sequqences for now 
#     subprocess.call('del *.pdb', shell=True)

#     if keys==[]:
#         keys=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
#     start=time.time()
#     for key in keys:
#         subprocess.call(f"./download_key.sh {key}", shell=True)
#     end = time.time()   
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/len(keys)} seconds")

#     return 

# def keyUniprotDownloadTime(keys=[]):

#     #i have no idea what a key looks like so it will be the same as the sequences for now 

#     if keys==[]:
#         keys=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
#     subprocess.call('del *.pdb', shell=True)

#     start=time.time()

#     for key in keys:
#         subprocess.call(f"./download_key_uniprot.sh {key}", shell=True)
#     end = time.time()   
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/len(keys)} seconds")
    
#     return 

# def alphafoldDownloadTime(n=99):
#     subprocess.call('del *.pdb', shell=True)

#     start = time.time()

#     subprocess.call(f"./download_alphafold.sh {n}")
#     end=time.time()
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/n} seconds")

#     return

# def alphafoldRandomDownloadTime(n=99):
#     subprocess.call('del *.pdb', shell=True)

#     start = time.time()
#     subprocess.call()
#     subprocess.call(f"./download_alphafold_random.sh {n}")
#     end=time.time()
#     change=len(glob.glob(".pdb"))

#     print(f"took {start-end} seconds to complete testing, where {change} PDB files were returned, each API call took on average {(start-end)/n} seconds")

#     return

if __name__ == "__main__":
    # valid_eps={"af_random":alphafoldRandomDownloadTime,"af":alphafoldDownloadTime,"key_uniprot":keyUniprotDownloadTime,"key":keyDownloadTime,"sequence":sequenceDownloadTime,"uniprot_random_cache":uniprotRandomDownloadCacheTime,"uniprot_random":uniprotRandomDownloadTime,"uniprot_cache":uniprotSimpleDownloadCacheTime,"uniprot":uniprotSimpleDownloadTime,"upload":pdbUploadTime}
    repeated_calls={"af_random":"download_alphafold_random","af":"download_alphafold","uniprot_random_cache":"download_cache_random","uniprot_random":"download_pdb_random","uniprot_cache":"download_cache","uniprot":"download_pdb","upload":"upload_pdb"}
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
