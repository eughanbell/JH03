import logging
import unittest
logger = logging.getLogger(__name__)

from urllib.request import urlopen

from src.uniprot import request_uniprot_file
from src.uniprot import parse_uniprot_xml
from src.uniprot import uniprot_get_entries

class TestUniprot(unittest.TestCase):
    def test_request_uniprot_file(self):
        #Valid A
        validTest = request_uniprot_file("p02070","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p02070.xml")
        self.assertEqual(validTest, comparison.read())

        #Valid B
        validTest = request_uniprot_file("p06213","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/p06213.xml")
        self.assertEqual(validTest, comparison.read())

        #Valid C
        validTest = request_uniprot_file("a0pk11","xml")
        comparison = urlopen("https://rest.uniprot.org/uniprotkb/a0pk11.xml")
        self.assertEqual(validTest, comparison.read())

        #Invalid uniprot_id
        self.assertEqual(request_uniprot_file("ImNotAnId", "xml"), None)

        #Invalid filetype
        self.assertEqual(request_uniprot_file("p02070", "ImNotAFiletype"), None)

        #Non-string uniprot_id
        self.assertEqual(request_uniprot_file(2070, "xml"), None)

        #Non-xml filetype
        self.assertEqual(request_uniprot_file("p02070", "html"), None)

    def test_parse_uniprot_xml(self):
        #Valid A
        test = parse_uniprot_xml("A0A7M7QR98")
        comparison = [{'dbname': 'EnsemblMetazoa', 'dict': {'id': 'XM_032597514', 'protein sequence ID': 'XP_032453405', 'gene ID': 'LOC100119623'}}, {'dbname': 'Proteomes', 'dict': {'id': 'UP000002358', 'component': 'Chromosome 2'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005886', 'term': 'C:plasma membrane', 'evidence': 'ECO:0007669', 'project': 'InterPro'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0007411', 'term': 'P:axon guidance', 'evidence': 'ECO:0007669', 'project': 'InterPro'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0007155', 'term': 'P:cell adhesion', 'evidence': 'ECO:0007669', 'project': 'InterPro'}}, {'dbname': 'CDD', 'dict': {'id': 'cd00063', 'entry name': 'FN3', 'match status': '2'}}, {'dbname': 'CDD', 'dict': {'id': 'cd00096', 'entry name': 'Ig', 'match status': '1'}}, {'dbname': 'Gene3D', 'dict': {'id': '2.60.40.10', 'entry name': 'Immunoglobulins', 'match status': '7'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR043204', 'entry name': 'Basigin-like'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR003961', 'entry name': 'FN3_dom'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR036116', 'entry name': 'FN3_sf'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR007110', 'entry name': 'Ig-like_dom'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR036179', 'entry name': 'Ig-like_dom_sf'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR013783', 'entry name': 'Ig-like_fold'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR013098', 'entry name': 'Ig_I-set'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR003599', 'entry name': 'Ig_sub'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR003598', 'entry name': 'Ig_sub2'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR013106', 'entry name': 'Ig_V-set'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR10075', 'entry name': 'BASIGIN RELATED', 'match status': '1'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR10075:SF92', 'entry name': 'PROTEIN TURTLE', 'match status': '1'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF00041', 'entry name': 'fn3', 'match status': '2'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF07679', 'entry name': 'I-set', 'match status': '1'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF13927', 'entry name': 'Ig_3', 'match status': '2'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF07686', 'entry name': 'V-set', 'match status': '1'}}, {'dbname': 'SMART', 'dict': {'id': 'SM00060', 'entry name': 'FN3', 'match status': '2'}}, {'dbname': 'SMART', 'dict': {'id': 'SM00409', 'entry name': 'IG', 'match status': '5'}}, {'dbname': 'SMART', 'dict': {'id': 'SM00408', 'entry name': 'IGc2', 'match status': '5'}}, {'dbname': 'SMART', 'dict': {'id': 'SM00406', 'entry name': 'IGv', 'match status': '4'}}, {'dbname': 'SUPFAM', 'dict': {'id': 'SSF49265', 'entry name': 'Fibronectin type III', 'match status': '1'}}, {'dbname': 'SUPFAM', 'dict': {'id': 'SSF48726', 'entry name': 'Immunoglobulin', 'match status': '5'}}, {'dbname': 'PROSITE', 'dict': {'id': 'PS50853', 'entry name': 'FN3', 'match status': '2'}}, {'dbname': 'PROSITE', 'dict': {'id': 'PS50835', 'entry name': 'IG_LIKE', 'match status': '5'}}]
        self.assertEqual(test, comparison)

        #Valid B
        test = parse_uniprot_xml("Q9NR00")
        comparison = [{'dbname': 'EMBL', 'dict': {'id': 'AF268037', 'protein sequence ID': 'AAF78961.1', 'molecule type': 'mRNA'}}, {'dbname': 'EMBL', 'dict': {'id': 'AC022733', 'status': 'NOT_ANNOTATED_CDS', 'molecule type': 'Genomic_DNA'}}, {'dbname': 'EMBL', 'dict': {'id': 'BC020623', 'protein sequence ID': 'AAH20623.1', 'molecule type': 'mRNA'}}, {'dbname': 'EMBL', 'dict': {'id': 'BC021672', 'protein sequence ID': 'AAH21672.1', 'molecule type': 'mRNA'}}, {'dbname': 'CCDS', 'dict': {'id': 'CCDS6115.1'}}, {'dbname': 'RefSeq', 'dict': {'id': 'NP_064515.1', 'nucleotide sequence ID': 'NM_020130.4'}}, {'dbname': 'AlphaFoldDB', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'BMRB', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'BioGRID', 'dict': {'id': '121222', 'interactions': '4'}}, {'dbname': 'IntAct', 'dict': {'id': 'Q9NR00', 'interactions': '2'}}, {'dbname': 'STRING', 'dict': {'id': '9606.ENSP00000319914'}}, {'dbname': 'iPTMnet', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'PhosphoSitePlus', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'BioMuta', 'dict': {'id': 'TCIM'}}, {'dbname': 'DMDM', 'dict': {'id': '296434443'}}, {'dbname': 'MassIVE', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'PaxDb', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'PeptideAtlas', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'ProteomicsDB', 'dict': {'id': '82240'}}, {'dbname': 'Antibodypedia', 'dict': {'id': '23908', 'antibodies': '88 antibodies from 20 providers'}}, {'dbname': 'DNASU', 'dict': {'id': '56892'}}, {'dbname': 'Ensembl', 'dict': {'id': 'ENST00000315792.5', 'protein sequence ID': 'ENSP00000319914.3', 'gene ID': 'ENSG00000176907.5'}}, {'dbname': 'GeneID', 'dict': {'id': '56892'}}, {'dbname': 'KEGG', 'dict': {'id': 'hsa:56892'}}, {'dbname': 'MANE-Select', 'dict': {'id': 'ENST00000315792.5', 'protein sequence ID': 'ENSP00000319914.3', 'RefSeq nucleotide sequence ID': 'NM_020130.5', 'RefSeq protein sequence ID': 'NP_064515.2'}}, {'dbname': 'UCSC', 'dict': {'id': 'uc003xnq.3', 'organism name': 'human'}}, {'dbname': 'AGR', 'dict': {'id': 'HGNC:1357'}}, {'dbname': 'CTD', 'dict': {'id': '56892'}}, {'dbname': 'DisGeNET', 'dict': {'id': '56892'}}, {'dbname': 'GeneCards', 'dict': {'id': 'TCIM'}}, {'dbname': 'HGNC', 'dict': {'id': 'HGNC:1357', 'gene designation': 'TCIM'}}, {'dbname': 'HPA', 'dict': {'id': 'ENSG00000176907', 'expression patterns': 'Low tissue specificity'}}, {'dbname': 'MIM', 'dict': {'id': '607702', 'type': 'gene'}}, {'dbname': 'neXtProt', 'dict': {'id': 'NX_Q9NR00'}}, {'dbname': 'OpenTargets', 'dict': {'id': 'ENSG00000176907'}}, {'dbname': 'PharmGKB', 'dict': {'id': 'PA25962'}}, {'dbname': 'VEuPathDB', 'dict': {'id': 'HostDB:ENSG00000176907'}}, {'dbname': 'eggNOG', 'dict': {'id': 'ENOG502S1N0', 'taxonomic scope': 'Eukaryota'}}, {'dbname': 'GeneTree', 'dict': {'id': 'ENSGT00390000003458'}}, {'dbname': 'HOGENOM', 'dict': {'id': 'CLU_172922_0_0_1'}}, {'dbname': 'InParanoid', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'OMA', 'dict': {'id': 'ILDTDQD'}}, {'dbname': 'OrthoDB', 'dict': {'id': '3973693at2759'}}, {'dbname': 'PhylomeDB', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'TreeFam', 'dict': {'id': 'TF338287'}}, {'dbname': 'PathwayCommons', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'SignaLink', 'dict': {'id': 'Q9NR00'}}, {'dbname': 'BioGRID-ORCS', 'dict': {'id': '56892', 'hits': '12 hits in 1127 CRISPR screens'}}, {'dbname': 'GeneWiki', 'dict': {'id': 'C8orf4'}}, {'dbname': 'GenomeRNAi', 'dict': {'id': '56892'}}, {'dbname': 'Pharos', 'dict': {'id': 'Q9NR00', 'development level': 'Tbio'}}, {'dbname': 'PRO', 'dict': {'id': 'PR:Q9NR00'}}, {'dbname': 'Proteomes', 'dict': {'id': 'UP000005640', 'component': 'Chromosome 8'}}, {'dbname': 'RNAct', 'dict': {'id': 'Q9NR00', 'molecule type': 'Protein'}}, {'dbname': 'Bgee', 'dict': {'id': 'ENSG00000176907', 'expression patterns': 'Expressed in parotid gland and 177 other tissues'}}, {'dbname': 'Genevisible', 'dict': {'id': 'Q9NR00', 'organism ID': 'HS'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005737', 'term': 'C:cytoplasm', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005829', 'term': 'C:cytosol', 'evidence': 'ECO:0000314', 'project': 'HPA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0016607', 'term': 'C:nuclear speck', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005730', 'term': 'C:nucleolus', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005654', 'term': 'C:nucleoplasm', 'evidence': 'ECO:0000314', 'project': 'HPA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005634', 'term': 'C:nucleus', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005886', 'term': 'C:plasma membrane', 'evidence': 'ECO:0000314', 'project': 'HPA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005112', 'term': 'F:Notch binding', 'evidence': 'ECO:0000353', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0006915', 'term': 'P:apoptotic process', 'evidence': 'ECO:0007669', 'project': 'UniProtKB-KW'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0034605', 'term': 'P:cellular response to heat', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0002264', 'term': 'P:endothelial cell activation involved in immune response', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0043066', 'term': 'P:negative regulation of apoptotic process', 'evidence': 'ECO:0000314', 'project': 'CAFA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0045746', 'term': 'P:negative regulation of Notch signaling pathway', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:1901224', 'term': 'P:positive regulation of NIK/NF-kappaB signaling', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0010739', 'term': 'P:positive regulation of protein kinase A signaling', 'evidence': 'ECO:0000314', 'project': 'CAFA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:1900020', 'term': 'P:positive regulation of protein kinase C activity', 'evidence': 'ECO:0000314', 'project': 'CAFA'}}, {'dbname': 'GO', 'dict': {'id': 'GO:1902806', 'term': 'P:regulation of cell cycle G1/S phase transition', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0043620', 'term': 'P:regulation of DNA-templated transcription in response to stress', 'evidence': 'ECO:0000314', 'project': 'UniProtKB'}}, {'dbname': 'GO', 'dict': {'id': 'GO:1903706', 'term': 'P:regulation of hemopoiesis', 'evidence': 'ECO:0007669', 'project': 'Ensembl'}}, {'dbname': 'DisProt', 'dict': {'id': 'DP00372'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR020282', 'entry name': 'Avpi1/C8orf4_dom'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR039580', 'entry name': 'Tcim'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR32358', 'entry name': 'TRANSCRIPTIONAL AND IMMUNE RESPONSE REGULATOR', 'match status': '1'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR32358:SF1', 'entry name': 'TRANSCRIPTIONAL AND IMMUNE RESPONSE REGULATOR', 'match status': '1'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF15063', 'entry name': 'TC1', 'match status': '1'}}]
        self.assertEqual(test, comparison)

        #Valid C
        test = parse_uniprot_xml("P00022")
        comparison = [{'dbname': 'PIR', 'dict': {'id': 'A00019', 'entry name': 'CCST'}}, {'dbname': 'AlphaFoldDB', 'dict': {'id': 'P00022'}}, {'dbname': 'SMR', 'dict': {'id': 'P00022'}}, {'dbname': 'iPTMnet', 'dict': {'id': 'P00022'}}, {'dbname': 'Ensembl', 'dict': {'id': 'ENSCSRT00000024116', 'protein sequence ID': 'ENSCSRP00000023105', 'gene ID': 'ENSCSRG00000017375'}}, {'dbname': 'Proteomes', 'dict': {'id': 'UP000694403', 'component': 'Unplaced'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0005758', 'term': 'C:mitochondrial intermembrane space', 'evidence': 'ECO:0007669', 'project': 'UniProtKB-SubCell'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0070469', 'term': 'C:respirasome', 'evidence': 'ECO:0007669', 'project': 'UniProtKB-KW'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0009055', 'term': 'F:electron transfer activity', 'evidence': 'ECO:0007669', 'project': 'InterPro'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0020037', 'term': 'F:heme binding', 'evidence': 'ECO:0007669', 'project': 'InterPro'}}, {'dbname': 'GO', 'dict': {'id': 'GO:0046872', 'term': 'F:metal ion binding', 'evidence': 'ECO:0007669', 'project': 'UniProtKB-KW'}}, {'dbname': 'Gene3D', 'dict': {'id': '1.10.760.10', 'entry name': 'Cytochrome c-like domain', 'match status': '1'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR009056', 'entry name': 'Cyt_c-like_dom'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR036909', 'entry name': 'Cyt_c-like_dom_sf'}}, {'dbname': 'InterPro', 'dict': {'id': 'IPR002327', 'entry name': 'Cyt_c_1A/1B'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR11961', 'entry name': 'CYTOCHROME C', 'match status': '1'}}, {'dbname': 'PANTHER', 'dict': {'id': 'PTHR11961:SF12', 'entry name': 'CYTOCHROME C-RELATED', 'match status': '1'}}, {'dbname': 'Pfam', 'dict': {'id': 'PF00034', 'entry name': 'Cytochrom_C', 'match status': '1'}}, {'dbname': 'PRINTS', 'dict': {'id': 'PR00604', 'entry name': 'CYTCHRMECIAB'}}, {'dbname': 'SUPFAM', 'dict': {'id': 'SSF46626', 'entry name': 'Cytochrome c', 'match status': '1'}}, {'dbname': 'PROSITE', 'dict': {'id': 'PS51007', 'entry name': 'CYTC', 'match status': '1'}}]
        self.assertEqual(test, comparison)

        #Invalid uniprot_id
        test = parse_uniprot_xml("ImNotAnId")
        self.assertEqual(test, [])

        #Non-string uniprot_id
        test = parse_uniprot_xml(2000)
        self.assertEqual(test, [])

    def test_uniprot_get_entries(self):
        #Valid A
        test = uniprot_get_entries("O79680")
        comparison = 'O79680'
        self.assertEqual(test[0].entry_data["id"], comparison)

        #Valid B
        test = uniprot_get_entries("T1K7Y0")
        comparison = 'T1K7Y0'
        self.assertEqual(test[0].entry_data["id"], comparison)

        #Valid C
        test = uniprot_get_entries("K7GET2")
        comparison = 'K7GET2'
        self.assertEqual(test[0].entry_data["id"], comparison)

        #Invalid uniprot_id
        test = uniprot_get_entries("ImNotAnId")
        self.assertEqual(test, [])

        #Non-string uniprot_id
        test = uniprot_get_entries(12345)
        self.assertEqual(test, [])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
