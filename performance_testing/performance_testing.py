import subprocess
from subprocess import call
import time,sys,glob,json,requests,os
from scripts.incrementScript import incrementScript
from scripts.randomScript import randomScript
from scripts.manualScript import manualScript

if not os.path.isdir("pdb_files"):
   os.makedirs("pdb_files")


def mainManualScript(s,f):
    #split args by , delimeter
    params=s.split(",")
    time=manualScript(f,params[0],params[1],params[2])
    no_of_pdbs=len(glob.glob("pdb_files/*.pdb"))
    print(f"This testing took {time} seconds, and returning {no_of_pdbs} PDB files, for an average of roughly {time/no_of_pdbs} seconds per successful API call")

def mainRandomScript(s):
    params=s.split(",")
    time=randomScript(params[0],params[1])
    no_of_pdbs=len(glob.glob("pdb_files/*.pdb"))
    print(f"This testing took {time} seconds, and returning {no_of_pdbs} PDB files, for an average of roughly {time/no_of_pdbs} seconds per successful API call")


def mainIncrementScript(s):
    params=s.split(",")
    time=incrementScript(params[0],params[1])
    no_of_pdbs=len(glob.glob("pdb_files/*.pdb"))
    print(f"This testing took {time} seconds, and returning {no_of_pdbs} PDB files, for an average of roughly {time/no_of_pdbs} seconds per successful API call")




if __name__ == "__main__":
    increment_calls=json.load(open("increments.json"))
    random_calls=json.load(open("randoms.json"))
    manual_calls=json.load(open("manualscripts.json"))

    if len(sys.argv)==1:
        print("Please select an endpoint to test!")
    elif len(sys.argv)==3 and str(sys.argv[2]).endswith(".txt"): #check if they pass a text file of uniprot ids
        choice=sys.argv[1]
        if choice in manual_calls:
            mainManualScript(manual_calls[choice],sys.argv[2])
        else:
            print(f"endpoint {sys.argv[1]} is not valid, Please refer to the list of valid inputs if you are confused")
    else:
        #list of sys args that correspond to endpoints
        endpoints = sys.argv[1:]
        for endpoint in endpoints:
            if endpoint in increment_calls:
                mainIncrementScript(increment_calls[endpoint])
            elif endpoint in random_calls:
                mainRandomScript(random_calls[endpoint])
            else:
                print(f"endpoint {endpoint} is not valid, Please refer to the list of valid inputs if you are confused")

