import datetime
from unittest import TestCase
from molecupy.pdbfile import PdbFile, PdbRecord
from molecupy.pdbdatafile import *

class PdbDataFileTest(TestCase):

    def setUp(self):
        self.empty = PdbDataFile(PdbFile(""))



class PdbdataFilePropertiesTests(PdbDataFileTest):

    def test_has_pdb_file(self):
        self.assertIsInstance(self.empty.pdb_file, PdbFile)


    def test_repr(self):
        self.assertRegex(
         str(self.empty),
         r"<PdbDataFile \(([^\s]{4})\)>"
        )



class DateFromStringTests(TestCase):

    def test_can_get_date_from_string(self):
        self.assertEqual(
         date_from_string("01-JAN-00"),
         datetime.datetime(2000, 1, 1).date()
        )
        self.assertEqual(
         date_from_string("28-SEP-99"),
         datetime.datetime(1999, 9, 28).date()
        )



class RecordMergingTests(TestCase):

    def setUp(self):
        self.records = [PdbRecord(l, 1) for l in [
         "0123456789",
         "abcdefghij",
         "0123456789"
        ]]

        self.punc_records = [PdbRecord(l, 1) for l in [
         "0123, 456789",
         "abcd  efghij",
         "0123; 456789"
        ]]


    def test_can_merge_records(self):
        self.assertEqual(
         merge_records(self.records, 5),
         "56789 fghij 56789"
        )
        self.assertEqual(
         merge_records(self.records, 8),
         "89 ij 89"
        )


    def test_can_vary_join(self):
        self.assertEqual(
         merge_records(self.records, 5, join=""),
         "56789fghij56789"
        )
        self.assertEqual(
         merge_records(self.records, 8, join="."),
         "89.ij.89"
        )


    def test_can_condense(self):
        self.assertEqual(
         merge_records(self.punc_records, 2),
         "23,456789 cd efghij 23;456789"
        )


    def test_can_ignore_consensors(self):
        self.assertEqual(
         merge_records(self.punc_records, 2, dont_condense=","),
         "23, 456789 cd efghij 23;456789"
        )
        self.assertEqual(
         merge_records(self.punc_records, 2, dont_condense=";"),
         "23,456789 cd efghij 23; 456789"
        )
        self.assertEqual(
         merge_records(self.punc_records, 2, dont_condense=";,"),
         "23, 456789 cd efghij 23; 456789"
        )
        self.assertEqual(
         merge_records(self.punc_records, 2, dont_condense=";, "),
         "23, 456789 cd  efghij 23; 456789"
        )


class RecordsToDictTests(TestCase):

    def test_can_make_dicts(self):
        records = [PdbRecord(l, 1) for l in [
         "COMPND    MOL_ID: A;",
         "COMPND   2 MOLECULE: MOLNAME;",
         "COMPND   3 CHAIN_: CHAINS;",
         "COMPND   4 MOL_ID: B;",
         "COMPND   5 MOLECULE: MOLNAME2;",
         "COMPND   6 CHAIN_: CHAINS2;"
        ]]
        self.assertEqual(
         records_to_token_value_dicts(records),
         [
          {"MOL_ID": "A", "MOLECULE": "MOLNAME", "CHAIN_": "CHAINS"},
          {"MOL_ID": "B", "MOLECULE": "MOLNAME2", "CHAIN_": "CHAINS2"}
         ]
        )


    def test_can_detect_numeric_fields(self):
        records = [PdbRecord(l, 1) for l in [
         "COMPND    MOL_ID: 1;",
         "COMPND   2 MOLECULE: MOLNAME;",
         "COMPND   3 CHAIN_: CHAINS;"
        ]]
        self.assertEqual(
         records_to_token_value_dicts(records),
         [
          {"MOL_ID": 1, "MOLECULE": "MOLNAME", "CHAIN_": "CHAINS"}
         ]
        )


    def test_can_detect_boolean_fields(self):
        records = [PdbRecord(l, 1) for l in [
         "COMPND    MOL_ID: 1;",
         "COMPND   2 MOLECULE: YES;",
         "COMPND   3 CHAIN_: NO;"
        ]]
        self.assertEqual(
         records_to_token_value_dicts(records),
         [
          {"MOL_ID": 1, "MOLECULE": True, "CHAIN_": False}
         ]
        )


    def test_can_split_chains_and_synonyms(self):
        records = [PdbRecord(l, 1) for l in [
         "COMPND    MOL_ID: 1;",
         "COMPND   2 CHAIN: A,B;",
         "COMPND   2 SYNONYM: BEEP, BOOP;"
        ]]
        self.assertEqual(
         records_to_token_value_dicts(records),
         [
          {"MOL_ID": 1, "CHAIN": ["A", "B"], "SYNONYM": ["BEEP", "BOOP"]}
         ]
        )



class HeaderRecordTests(PdbDataFileTest):

    def test_header_processing(self):
        data_file = PdbDataFile(PdbFile(
         "HEADER    LYASE                                   06-MAY-02   1LOL"
        ))
        self.assertEqual(data_file.classification, "LYASE")
        self.assertEqual(
         data_file.deposition_date,
         datetime.datetime(2002, 5, 6).date()
        )
        self.assertEqual(data_file.pdb_code, "1LOL")


    def test_missing_header_processing(self):
        self.assertEqual(self.empty.classification, None)
        self.assertEqual(self.empty.deposition_date, None)
        self.assertEqual(self.empty.pdb_code, None)



class ObslteRecordTests(PdbDataFileTest):

    def test_obslte_processing(self):
        data_file = PdbDataFile(PdbFile(
         "OBSLTE     30-SEP-93 1LOL      1SAM"
        ))
        self.assertTrue(data_file.is_obsolete)
        self.assertEqual(
         data_file.obsolete_date,
         datetime.datetime(1993, 9, 30).date()
        )
        self.assertEqual(
         data_file.replacement_code,
         "1SAM"
        )


    def test_missing_obslte_processing(self):
        self.assertFalse(self.empty.is_obsolete)
        self.assertEqual(self.empty.obsolete_date, None)
        self.assertEqual(self.empty.replacement_code, None)



class TitleRecordTests(PdbDataFileTest):

    def test_title_processing(self):
        data_file = PdbDataFile(PdbFile(
         "TITLE     CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE\n"
         "TITLE    2 COMPLEX WITH XMP"
        ))
        self.assertEqual(
         data_file.title,
         "CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE COMPLEX WITH XMP"
        )


    def test_missing_title_processing(self):
        self.assertEqual(self.empty.title, None)



class SplitRecordTests(PdbDataFileTest):

    def test_split_processing(self):
        data_file = PdbDataFile(PdbFile(
         "SPLIT      1VOQ 1VOR 1VOS 1VOU 1VOV 1VOW 1VOX 1VOY 1VP0 1VOZ 1VOY 1VP0 1VOZ 1VOZ\n"
         "SPLIT      1VOQ 1VOR 1VOS 1VOU 1VOV 1VOW 1VOX 1VOY 1VP0 1VOZ"
        ))
        self.assertEqual(
         data_file.split_codes,
         [
          "1VOQ", "1VOR", "1VOS", "1VOU", "1VOV", "1VOW",
          "1VOX", "1VOY", "1VP0", "1VOZ", "1VOY", "1VP0",
          "1VOZ", "1VOZ", "1VOQ", "1VOR", "1VOS", "1VOU",
          "1VOV", "1VOW", "1VOX", "1VOY", "1VP0", "1VOZ"
         ]
        )


    def test_missing_split_processing(self):
        self.assertEqual(self.empty.split_codes, [])



class CaveatRecordTests(PdbDataFileTest):

    def test_caveat_processing(self):
        data_file = PdbDataFile(PdbFile(
         "CAVEAT     1SAM    THE CRYSTAL TRANSFORMATION IS IN ERROR BUT IS\n"
         "CAVEAT   2 1SAM    UNCORRECTABLE AT THIS TIME"
        ))
        self.assertEqual(
         data_file.caveat,
         "THE CRYSTAL TRANSFORMATION IS IN ERROR BUT IS UNCORRECTABLE AT THIS TIME"
        )


    def test_missing_caveat_processing(self):
        self.assertEqual(self.empty.caveat, None)



class SourceRecordTests(PdbDataFileTest):

    def test_compnd_processing(self):
        data_file = PdbDataFile(PdbFile(
         "COMPND    MOL_ID: 1;\n"
         "COMPND   2 MOLECULE: OROTIDINE 5'-MONOPHOSPHATE DECARBOXYLASE;\n"
         "COMPND   3 CHAIN: A, B;\n"
         "COMPND   4 SYNONYM: OMP DECARBOXYLASE, OMPDCASE, OMPDECASE;\n"
         "COMPND   5 EC: 4.1.1.23;\n"
         "COMPND   6 ENGINEERED: YES;\n"
         "COMPND   7 MOL_ID: 2;\n"
         "COMPND   8 MOLECULE: OROTIDINE 5'-MONOPHOSPHATE DECARBOXYLASE\n"
         "COMPND   9 PLUS;"
        ))
        self.assertEqual(
         data_file.compounds,
         [
          {
           "MOL_ID": 1,
           "MOLECULE": "OROTIDINE 5'-MONOPHOSPHATE DECARBOXYLASE",
           "CHAIN": ["A", "B"],
           "SYNONYM": [
            "OMP DECARBOXYLASE",
            "OMPDCASE",
            "OMPDECASE"
           ],
           "EC": "4.1.1.23",
           "ENGINEERED": True
          }, {
           "MOL_ID": 2,
           "MOLECULE": "OROTIDINE 5'-MONOPHOSPHATE DECARBOXYLASE PLUS"
          }
         ]
        )


    def test_missing_compnd_processing(self):
        self.assertEqual(self.empty.compounds, [])



class SourceRecordTests(PdbDataFileTest):

    def test_source_processing(self):
        data_file = PdbDataFile(PdbFile(
         "SOURCE    MOL_ID: 1;\n"
         "SOURCE   2 ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER\n"
         "SOURCE   3 THERMAUTOTROPHICUS STR. DELTA H;\n"
         "SOURCE   4 ORGANISM_TAXID: 187420;\n"
         "SOURCE   5 STRAIN: DELTA H;\n"
         "SOURCE   6 EXPRESSION_SYSTEM: ESCHERICHIA COLI;\n"
         "SOURCE   7 EXPRESSION_SYSTEM_TAXID: 562;\n"
         "SOURCE   8 EXPRESSION_SYSTEM_PLASMID: PET15B\n"
        ))
        self.assertEqual(
         data_file.sources,
         [
          {
           "MOL_ID": 1,
           "ORGANISM_SCIENTIFIC": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
           "ORGANISM_TAXID": 187420,
           "STRAIN": "DELTA H",
           "EXPRESSION_SYSTEM": "ESCHERICHIA COLI",
           "EXPRESSION_SYSTEM_TAXID": 562,
           "EXPRESSION_SYSTEM_PLASMID": "PET15B"
          }
         ]
        )


    def test_missing_source_processing(self):
        self.assertEqual(self.empty.sources, [])
