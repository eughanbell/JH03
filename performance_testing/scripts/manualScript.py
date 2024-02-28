import os, requests,glob,time

def manualScript(file,endpoint="Retrieve_by_uniprot_id",cache=False,alphafold=False):
        pdbs_to_delete =glob.glob("pdb_files/*.pdb")
        print("Clearing existing pdb files")
        for file_path in pdbs_to_delete:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        with open(file, "r") as f:
            ids = [line.strip() for line in f]


        start=time.time()


        if cache==True:
            for i in range(2):
                if alphafold==True:
                        for id in ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}?db=alphafold")
                            with open(f"pdb_files/{i}.pdb","wb") as f:
                                f.write(r.contents)
                            if os.path.exists(f) and os.path.getsize(f) == 0:
                                os.remove(f) 
                else:
                        for id in ids:
                            r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}")
                            with open(f"pdb_files/{i}.pdb","wb") as f:
                                f.write(r.contents)
                            if os.path.exists(f) and os.path.getsize(f) == 0:
                                os.remove(f) 

        else: 
            if alphafold==True:
                for id in ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}?db=alphafold")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 
            else:
                for id in ids:
                    r = requests.get(f"http://0.0.0.0:8000/{endpoint}/{id}")
                    with open(f"pdb_files/{i}.pdb","wb") as f:
                        f.write(r.contents)
                    if os.path.exists(f) and os.path.getsize(f) == 0:
                        os.remove(f) 

        end=time.time()

        return (start-end)