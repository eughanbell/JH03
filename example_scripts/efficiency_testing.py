import subprocess
from subprocess import call
import time

def uniprotSimpleDownloadTime(n):
    #n = no of curl requests to make, must be greater than 10

    start=time.time()
    subprocess.call("./download_pdbs.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotSimpleDownloadCacheTime(n):
    #n = no of curl requests to make, must be greater than 10
    start=time.time()
    subprocess.call("./download_cache.sh"+str(n), shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def pdbUploadTime():
    start=time.time()
    subprocess.call("./upload_pdb.sh", shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotRandomDownloadTime(n):
    #n = no of curl requests to make, must be greater than 10
    start=time.time()
    subprocess.call("./download_pdbs_random.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotRandomDownloadCacheTime(n):
    #n = no of curl requests to make, must be greater than 10
    start=time.time()
    subprocess.call("./download_cache_random.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

#these are for WIP endpoints
def sequenceDownloadTime(n,sequences=[]):
    #pass theoretical list of working sequences. 
    if sequences==[]:
        sequences=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
    start=time.time()
    for sequence in sequences:
        subprocess.call(f"./download_sequence.sh {sequence}", shell=True)
    end = time.time()   
    print(f"took {start-end} seconds to complete")
    return 

def keyDownloadTime(n,keys=[]):
    #i have no idea what a key looks like so it will be the same as the sequqences for now 
    if keys==[]:
        keys=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
    start=time.time()
    for key in keys:
        subprocess.call(f"./download_key.sh {key}", shell=True)
    end = time.time()   
    print(f"took {start-end} seconds to complete")
    return 

def keyUniprotDownloadTime(n,keys=[]):
    #i have no idea what a key looks like so it will be the same as the sequences for now 
    if keys==[]:
        keys=["ESNFIESRNJFEIFNES","NESNFESNFESNOFESOFES","BESIFBNWADBIAWNDWIA","FNUIESFNHESIFOIES"]
    start=time.time()
    for key in keys:
        subprocess.call(f"./download_key_uniprot.sh {key}", shell=True)
    end = time.time()   
    print(f"took {start-end} seconds to complete")
    return 