import os, requests, glob,time

def incrementScript(cache=False,alphafold=False,n=99,endpoint="retrieve_by_uniprot_id"):
        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        start=time.time()
        if cache==True:
            for j in range(2):
                if alphafold==True: 

                    for i in range(10,n):
                        r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}?db=alphafold")
                        with open(f"pdb_files/{i}.pdb","wb") as f:
                            f.write(r.contents)
                        if os.path.exists(f) and os.path.getsize(f) == 0:
                            os.remove(f) 
                else:
                    for i in range(10,n):
                        r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}")
                        with open(f"pdb_files/{i}.pdb","wb") as f:
                            f.write(r.contents)
                        if os.path.exists(f) and os.path.getsize(f) == 0:
                            os.remove(f) 
        else:
            if alphafold==True: 

                for i in range(10,n):
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}?db=alphafold")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 
            else:
                for i in range(10,n):
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/p020{i}")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 
        end=time.time()
        return (start-end)