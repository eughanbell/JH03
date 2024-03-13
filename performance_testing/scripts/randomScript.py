import os, requests,glob,time,random

def randomScript(cache=False,alphafold=False,n=99,endpoint="retrieve_by_uniprot_id"):

        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

                
        r_ids = ["p" + ''.join([str(random.randint(0, 9)) for _ in range(5)])*n]
        start=time.time()

        if cache==True:
            for i in range(2):
                if alphafold==True:
                        for r_id in r_ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}?db=alphafold")
                            with open(f"pdb_files/{i}.pdb","wb") as f:
                                f.write(r.contents)
                            if os.path.exists(f) and os.path.getsize(f) == 0:
                                os.remove(f) 
                else:
                        for r_id in r_ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}")
                            with open(f"pdb_files/{i}.pdb","wb") as f:
                                f.write(r.contents)
                            if os.path.exists(f) and os.path.getsize(f) == 0:
                                os.remove(f) 

        else: 
            if alphafold==True:
                for r_id in r_ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}?db=alphafold")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 
            else:
                for r_id in r_ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{r_id}")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 

        end=time.time()

        return (start-end)