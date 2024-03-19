import os

def write_non_empty(id, content):
    path = f"pdb_files/{id}.pdb"
    with open(path,"wb+") as f:
        f.write(content)
        if os.path.exists(path) and os.path.getsize(path) == 0:
            os.remove(path) 
