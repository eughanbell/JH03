from PDBeEntry import PDBeEntry
from uniprot import uniprot_get_entries
import sys



entries = [entry for entry in uniprot_get_entries(uniprot_id=("p02070" if len(sys.argv)<2 else sys.argv[1])) if isinstance(entry, PDBeEntry)]
entries.sort()
for entry in entries:
    print(entry)