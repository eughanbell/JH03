import os, requests,glob,time
from .helper import write_non_empty

def manualScript(file,endpoint="retrieve_by_uniprot_id",cache=False,alphafold=False):
        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        
        with open(file, "r") as f:
            ids = [line.strip() for line in f]
            
        print("Requesting protein files")
        start=time.time()

        if cache==True:
            for i in range(2):
                if alphafold==True:
                        for id in ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}?db=alphafold")
                            write_non_empty(id, r.content)
                else:
                        for id in ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}")
                            write_non_empty(id, r.content)

        else: 
            if alphafold==True:
                for id in ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}?db=alphafold")
                    write_non_empty(id, r.content)
            else:
                for id in ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}")
                    write_non_empty(id, r.content)

        end=time.time()

        return (end-start)
