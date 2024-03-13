import os, requests,glob,time,random
from .helper import write_non_empty

def randomScript(cache=False,alphafold=False,n=99,endpoint="retrieve_by_uniprot_id"):

        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

                
        r_ids = ["p" + ''.join([str(random.randint(0, 9)) for _ in range(5)]) for _ in range(n)]
        print(r_ids)
        start=time.time()

        if cache==True:
            for i in range(2):
                if alphafold==True:
                        for r_id in r_ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}?db=alphafold")
                            write_non_empty(r_id, r.content)
                else:
                        for r_id in r_ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}")
                            write_non_empty(r_id, r.content)

        else: 
            if alphafold==True:
                for r_id in r_ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}?db=alphafold")
                    write_non_empty(r_id, r.content)
            else:
                for r_id in r_ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}")
                    write_non_empty(r_id, r.content)

        end=time.time()

        return (end-start)
