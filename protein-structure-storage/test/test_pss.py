import logging
import json
import unittest
from src.pss import *
from src.database_entries.afdb_entry import AFDBEntry
from src.database_entries.pdbe_entry import PDBeEntry


logger = logging.getLogger(__name__)
afdb_test_entry = AFDBEntry({'id': 'P02070'})
pdbe_test_entry = PDBeEntry({'id': '6II1', 'method': 'X-ray', 'resolution': '1.34 A', 'chains': 'B/D=1-145', 'protein_metadata': {'mass':15389, 'sequence_length':145, 'sequence': 'MVLSAADKGNVKAAWGKVGGHAAEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGAKVAAALTKAVEHLDDLPGALSELSDLHAHKLRVDPVNFKLLSHSLLVTLASHLPSDFTPAVHASLDKFLANVSTVLTSKYRPSD'}})


class Testpss(unittest.TestCase):
    
    def test_get_pdb_file(self):
        pdb_file1 = get_pdb_file('P02070', override_cache=True, source_dbs=None)
        self.assertNotEqual(afdb_test_entry.fetch(), pdb_file1, "Expected pdb file of a PDBe entry. Got an AFDB file.")
        self.assertEqual(pdbe_test_entry.fetch(), pdb_file1, "Recieved file does not match with test PDBe file")

        #TESTING source_dbs flag with AFDB
        pdb_file2 =  get_pdb_file('P02070', override_cache=True, source_dbs=["AFDB"])
        self.assertNotEqual(pdbe_test_entry.fetch(),  pdb_file2, "Expected pdb file of an AFDB entry. Got a PDBe file. Check source_dbs flag")
        self.assertEqual(afdb_test_entry.fetch(), pdb_file2, "Recieved file does not match with test AFDB file")

if __name__ == "__main__":
    unittest.main()


