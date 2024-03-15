import os, requests, glob,time
from .helper import write_non_empty

def incrementScript(cache=False,alphafold=False,n=99,endpoint="retrieve_by_uniprot_id"):
        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        print("Requesting protein files")
        start=time.time()
        if cache==True:
            for j in range(2):
                if alphafold==True: 

                    for i in range(10,n):
                        r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}?db=alphafold")
                        write_non_empty(i, r.content)
                else:
                    for i in range(10,n):
                        r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}")
                        write_non_empty(i, r.content)
        else:
            if alphafold==True: 

                for i in range(10,n):
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}?db=alphafold")
                    write_non_empty(i, r.content)
            else:
                for i in range(10,n):
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}")
                    write_non_empty(i, r.content)
        end=time.time()
        return (end-start)
