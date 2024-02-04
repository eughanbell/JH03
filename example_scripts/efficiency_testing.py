import subprocess
from subprocess import call
import time

def uniprotSimpleDownloadTime(n):
    #n = no of curl requests to make, must be greater than 10

    start=time.time()
    subprocess.call("download_pdbs.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotSimpleDownloadCacheTime(n):
    #n = no of curl requests to make, must be greater than 10
    start=time.time()
    subprocess.call("download_cache.sh"+str(n), shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def pdbUploadTime():
    start=time.time()
    subprocess.call("upload_pdb.sh", shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotRandomDownloadTime(n):
    #n = no of curl requests to make, must be greater than 10
    start=time.time()
    subprocess.call("download_pdbs_random.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 

def uniprotRandomDownloadCacheTime(n):
    #n = no of curl requests to make, must be greater than 10

    start=time.time()
    subprocess.call("download_cache_random.sh"+str(n),shell=True)
    end=time.time()
    print(f"took {start-end} seconds to complete")
    return 