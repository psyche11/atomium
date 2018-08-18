from copy import deepcopy
from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from atomium.files.pdb import *

class PdbStringToPdbDictTests(TestCase):

    def test_can_turn_pdb_string_to_pdb_dict(self):
        lines = [
         " ",
         "REC1  CONTENTS1", "REC2   CONTENTS2", "REC2  CONTENTS3",
         "REC3  CONTENTS4 ...     ", "RECCC4CONTENTS5 ..",
        ]
        self.assertEqual(pdb_string_to_pdb_dict("\n".join(lines)), {
         "REC1": ["CONTENTS1"],
         "REC2": [" CONTENTS2", "CONTENTS3"],
         "REC3": ["CONTENTS4 ..."],
         "RECCC4": ["CONTENTS5 .."]
        })



class PdbDictToDataDictTests(TestCase):

    @patch("atomium.files.pdb.update_description_dict")
    @patch("atomium.files.pdb.update_experiment_dict")
    @patch("atomium.files.pdb.update_quality_dict")
    @patch("atomium.files.pdb.update_geometry_dict")
    @patch("atomium.files.pdb.update_models_list")
    def test_can_convert_pdb_dict_to_data_dict(self, mock_mdls, mock_geo, mock_qual, mock_exp, mock_desc):
        self.assertEqual(pdb_dict_to_data_dict({"A": "B"}), DATA_DICT)
        mock_desc.assert_called_with({"A": "B"}, DATA_DICT)
        mock_exp.assert_called_with({"A": "B"}, DATA_DICT)
        mock_qual.assert_called_with({"A": "B"}, DATA_DICT)
        mock_geo.assert_called_with({"A": "B"}, DATA_DICT)
        mock_mdls.assert_called_with({"A": "B"}, DATA_DICT)



class DescriptionDictUpdatingTests(TestCase):

    @patch("atomium.files.pdb.extract_header")
    @patch("atomium.files.pdb.extract_title")
    @patch("atomium.files.pdb.extract_keywords")
    @patch("atomium.files.pdb.extract_authors")
    def test_can_update_description_dict(self, mock_aut, mock_key, mock_tit, mock_hed):
        d = deepcopy(DATA_DICT)
        pdb_dict = {"PDB": "DICT"}
        update_description_dict(pdb_dict, d)
        mock_hed.assert_called_with(pdb_dict, d["description"])
        mock_tit.assert_called_with(pdb_dict, d["description"])
        mock_key.assert_called_with(pdb_dict, d["description"])
        mock_aut.assert_called_with(pdb_dict, d["description"])



class ExperimentDictUpdatingTests(TestCase):

    @patch("atomium.files.pdb.extract_technique")
    @patch("atomium.files.pdb.extract_source")
    def test_can_update_experiment_dict(self, mock_src, mock_tech):
        d = deepcopy(DATA_DICT)
        pdb_dict = {"PDB": "DICT"}
        update_experiment_dict(pdb_dict, d)
        mock_src.assert_called_with(pdb_dict, d["experiment"])
        mock_tech.assert_called_with(pdb_dict, d["experiment"])



class QualityDictUpdatingTests(TestCase):

    @patch("atomium.files.pdb.extract_resolution_remark")
    @patch("atomium.files.pdb.extract_rvalue_remark")
    def test_can_update_quality_dict(self, mock_rfac, mock_res):
        d = deepcopy(DATA_DICT)
        pdb_dict = {"PDB": "DICT"}
        update_quality_dict(pdb_dict, d)
        mock_res.assert_called_with(pdb_dict, d["quality"])
        mock_rfac.assert_called_with(pdb_dict, d["quality"])



class GeometryDictUpdatingTests(TestCase):

    @patch("atomium.files.pdb.extract_assembly_remark")
    def test_can_update_quality_dict(self, mock_ass):
        d = deepcopy(DATA_DICT)
        pdb_dict = {"PDB": "DICT"}
        update_geometry_dict(pdb_dict, d)
        mock_ass.assert_called_with(pdb_dict, d["geometry"])



class ModelListUpdatingTests(TestCase):

    @patch("atomium.files.pdb.atom_line_to_atom_dict")
    @patch("atomium.files.pdb.generate_higher_structures")
    @patch("atomium.files.pdb.assign_anisou")
    @patch("atomium.files.pdb.extract_sequence")
    @patch("atomium.files.pdb.extract_connections")
    def test_can_update_single_model(self, mock_con, mock_seq, mock_an, mock_gen, mock_at):
        pdb_dict = {"ATOM": ["at1", "at2", "at3"], "HETATM": ["ht1", "ht2", "ht3"]}
        data_dict = {"models": []}
        mock_at.side_effect = ({"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6})
        update_models_list(pdb_dict, data_dict)
        for a in pdb_dict["ATOM"]:
            mock_at.assert_any_call(a)
        for a in pdb_dict["HETATM"]:
            mock_at.assert_any_call(a, polymer=False)
        self.assertEqual(data_dict, {"models": [{
         "atoms": [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}],
         "chains": [], "residues": [], "ligands": [], "connections": []
        }]})
        mock_gen.assert_called_with(data_dict["models"])
        mock_an.assert_called_with(pdb_dict, data_dict["models"])
        mock_seq.assert_called_with(pdb_dict, data_dict["models"])
        mock_con.assert_called_with(pdb_dict, data_dict["models"])


    @patch("atomium.files.pdb.atom_line_to_atom_dict")
    @patch("atomium.files.pdb.generate_higher_structures")
    @patch("atomium.files.pdb.assign_anisou")
    @patch("atomium.files.pdb.extract_sequence")
    @patch("atomium.files.pdb.extract_connections")
    def test_can_update_multiple_model(self, mock_con, mock_seq, mock_an, mock_gen, mock_at):
        pdb_dict = {"ATOM": ["at1", "at2", "at3"], "HETATM": ["ht1", "ht2", "ht3"]}
        data_dict = {"models": []}
        mock_at.side_effect = ({"id": 1}, {"id": 2}, {"id": 1}, {"id": 4}, {"id": 5}, {"id": 4})
        update_models_list(pdb_dict, data_dict)
        for a in pdb_dict["ATOM"]:
            mock_at.assert_any_call(a)
        for a in pdb_dict["HETATM"]:
            mock_at.assert_any_call(a, polymer=False)
        self.assertEqual(data_dict, {"models": [{
         "atoms": [{"id": 1}, {"id": 2}, {"id": 4}, {"id": 5}],
         "chains": [], "residues": [], "ligands": [], "connections": []
        }, {
         "atoms": [{"id": 1}, {"id": 4}],
         "chains": [], "residues": [], "ligands": [], "connections": []
        }]})
        mock_gen.assert_called_with(data_dict["models"])
        mock_an.assert_called_with(pdb_dict, data_dict["models"])
        mock_seq.assert_called_with(pdb_dict, data_dict["models"])
        mock_con.assert_called_with(pdb_dict, data_dict["models"])



class HeaderExtractionTests(TestCase):

    def setUp(self):
        self.d = {"code": None, "deposition_date": None, "classification": None}


    def test_can_extract_no_header(self):
        extract_header({"TITLE": ["1"]}, self.d)
        self.assertEqual(self.d, {"code": None, "deposition_date": None, "classification": None})


    def test_can_extract_empty_header(self):
        extract_header({"HEADER": [" " * 74]}, self.d)
        self.assertEqual(self.d, {"code": None, "deposition_date": None, "classification": None})


    def test_can_extract_header(self):
        extract_header({"HEADER": [
         "    UNKNOWN FUNCTION" + " " * 24 + "21-AUG-17   6AR7" + " " * 14
        ]}, self.d)
        self.assertEqual(self.d, {
         "code": "6AR7", "deposition_date": date(2017, 8, 21), "classification": "UNKNOWN FUNCTION"
        })



class TitleExtractionTests(TestCase):

    def test_missing_title_extraction(self):
        d = {"title": None}
        extract_title({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"title": None})


    @patch("atomium.files.pdb.merge_lines")
    def test_title_extraction(self, mock_merge):
        d = {"title": None}
        mock_merge.return_value = "TITLE TITLE TITLE"
        extract_title({"TITLE": ["TITLE     L1", "TITLE    2 L2"]}, d)
        mock_merge.assert_called_with(["TITLE     L1", "TITLE    2 L2"], 4)
        self.assertEqual(d["title"], "TITLE TITLE TITLE")



class KeywordExtractionTests(TestCase):

    def test_missing_keyword_extraction(self):
        d = {"keywords": []}
        extract_keywords({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"keywords": []})


    @patch("atomium.files.pdb.merge_lines")
    def test_keywords_extraction(self, mock_merge):
        d = {"keywords": []}
        mock_merge.return_value = "KEY1, KEY2, KEY3"
        extract_keywords({"KEYWDS": ["KEY     L1", "KEY    2 L2"]}, d)
        mock_merge.assert_called_with(["KEY     L1", "KEY    2 L2"], 4)
        self.assertEqual(d["keywords"], ["KEY1", "KEY2", "KEY3"])



class AuthorExtractionTests(TestCase):

    def test_missing_author_extraction(self):
        d = {"authors": []}
        extract_authors({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"authors": []})


    @patch("atomium.files.pdb.merge_lines")
    def test_authors_extraction(self, mock_merge):
        d = {"authors": []}
        mock_merge.return_value = "AT1, AT2, AT3"
        extract_authors({"AUTHOR": ["AT     L1", "AT    2 L2"]}, d)
        mock_merge.assert_called_with(["AT     L1", "AT    2 L2"], 4)
        self.assertEqual(d["authors"], ["AT1", "AT2", "AT3"])



class TechniqueExtractionTests(TestCase):

    def test_missing_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"technique": None})


    def test_empty_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"EXPDTA": ["     "]}, d)
        self.assertEqual(d, {"technique": None})


    def test_technique_extraction(self):
        d = {"technique": None}
        extract_technique({"EXPDTA": ["    X-RAY DIFFRACTION        "]}, d)
        self.assertEqual(d, {"technique": "X-RAY DIFFRACTION"})



class SourceExtractionTests(TestCase):

    def setUp(self): pass

    def test_missing_source_extraction(self):
        d = {"source_organism": None, "expression_system": None}
        extract_source({"HEADER": ["1"]}, d)
        self.assertEqual(d, {"source_organism": None, "expression_system": None})


    @patch("atomium.files.pdb.merge_lines")
    def test_empty_source_extraction(self, mock_merge):
        mock_merge.return_value = "JYVGBHUBBGYBHKJNHBK"
        d = {"source_organism": None, "expression_system": None}
        extract_source({"SOURCE": ["1", "2"]}, d)
        self.assertEqual(d, {"source_organism": None, "expression_system": None})
        mock_merge.assert_called_with(["1", "2"], 4)


    @patch("atomium.files.pdb.merge_lines")
    def test_empty_source_extraction(self, mock_merge):
        mock_merge.return_value = (
         "MOL_ID: 1;"
         " ORGANISM_SCIENTIFIC: METHANOTHERMOBACTER"
         " THERMAUTOTROPHICUS STR. DELTA H;"
         " ORGANISM_TAXID: 187420;"
         " STRAIN: DELTA H;"
         " EXPRESSION_SYSTEM: ESCHERICHIA COLI;"
         " EXPRESSION_SYSTEM_TAXID: 562;"
         " EXPRESSION_SYSTEM_PLASMID: PET15B"
        )
        d = {"source_organism": None, "expression_system": None}
        extract_source({"SOURCE": ["1", "2"]}, d)
        self.assertEqual(d, {
         "source_organism": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
         "expression_system": "ESCHERICHIA COLI"
        })
        mock_merge.assert_called_with(["1", "2"], 4)



class ResolutionExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = [
         "   1", "   1 BLAH BLAH.",
         "   2", "   2 RESOLUTION.    1.90 ANGSTROMS.",
         "  24", "  24 BLAH BLAH."
        ]


    def test_missing_remarks_extraction(self):
        d = {"resolution": None}
        extract_resolution_remark({"REMARK": self.remark_lines[:2]}, d)
        self.assertEqual(d, {"resolution": None})
        extract_resolution_remark({"ABC": []}, d)
        self.assertEqual(d, {"resolution": None})


    def test_empty_resolution_extraction(self):
        d = {"resolution": None}
        self.remark_lines[3] = "REMARK   2 RESOLUTION. NOT APPLICABLE."
        extract_resolution_remark({"REMARK": self.remark_lines[:2]}, d)
        self.assertEqual(d, {"resolution": None})


    def test_resolution_extraction(self):
        d = {"resolution": None}
        extract_resolution_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"resolution": 1.9})



class RvalueExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = [
         "   1", "   1 BLAH BLAH.",
         "   3   CROSS-VALIDATION METHOD          : THROUGHOUT",
         "   3   FREE R VALUE TEST SET SELECTION  : RANDOM",
         "   3   R VALUE            (WORKING SET) : 0.193",
         "   3   FREE R VALUE                     : 0.229",
         "   3   FREE R VALUE TEST SET SIZE   (%) : 4.900",
         "   3   FREE R VALUE TEST SET COUNT      : 1583",
         "   3   BIN R VALUE           (WORKING SET) : 0.2340 "
         "  24", "  24 BLAH BLAH."
        ]


    def test_missing_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        extract_resolution_remark({"REMARK": self.remark_lines[:2]}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})
        extract_rvalue_remark({"ABC": []}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})


    def test_empty_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        self.remark_lines[4] = self.remark_lines[4][:-7]
        self.remark_lines[5] = self.remark_lines[5][:-7]
        extract_rvalue_remark({"REMARK": self.remark_lines[:2]}, d)
        self.assertEqual(d, {"rvalue": None, "rfree": None})


    def test_rvalue_extraction(self):
        d = {"rvalue": None, "rfree": None}
        extract_rvalue_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"rvalue": 0.193, "rfree": 0.229})



class BiomoleculeExtractionTests(TestCase):

    def setUp(self):
        self.remark_lines = [
         "   1 BLAH BLAH.",
         " 350",
         " 350 BIOMOLECULE: 1",
         " 350 SOFTWARE DETERMINED QUATERNARY STRUCTURE: DIMERIC",
         " 350 SOFTWARE USED: PISA",
         " 350 TOTAL BURIED SURFACE AREA: 1650 ANGSTROM**2",
         " 350 SURFACE AREA OF THE COMPLEX: 4240 ANGSTROM**2",
         " 350 APPLY THE FOLLOWING TO CHAINS: G, H",
         " 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         " 350   BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
         " 350   BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
         " 350",
         " 350 BIOMOLECULE: 5",
         " 350 SOFTWARE DETERMINED QUATERNARY STRUCTURE: DODECAMERIC",
         " 350 SOFTWARE USED: PISA",
         " 350 TOTAL BURIED SURFACE AREA: 21680 ANGSTROM**2",
         " 350 SURFACE AREA OF THE COMPLEX: 12240 ANGSTROM**2",
         " 350 CHANGE IN SOLVENT FREE ENERGY: -332.0 KCAL/MOL",
         " 350 APPLY THE FOLLOWING TO CHAINS: E, F, G, H,",
         " 350                    AND CHAINS: J, K, L",
         " 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         " 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000",
         " 350   BIOMT3   1  0.000000  0.000000  1.000000        0.00000",
         " 350   BIOMT1   2 -0.500000 -0.866025  0.000000        0.00000",
         " 350   BIOMT2   2  0.866025 -0.500000  0.000000        0.00000",
         " 350   BIOMT3   2  0.000000  0.000000  1.000000        0.00000",
         "  24",
         "  24 BLAH BLAH."
        ]


    def test_missing_biomolecules_extraction(self):
        d = {"assemblies": []}
        extract_assembly_remark({"REMARK": self.remark_lines[-2:]}, d)
        self.assertEqual(d, {"assemblies": []})


    @patch("atomium.files.pdb.assembly_lines_to_assembly_dict")
    def test_biomolecules_extraction(self, mock_dict):
        mock_dict.side_effect = "AB"
        d = {"assemblies": []}
        extract_assembly_remark({"REMARK": self.remark_lines}, d)
        self.assertEqual(d, {"assemblies": ["A", "B"]})
        mock_dict.assert_any_call(self.remark_lines[2:12])
        mock_dict.assert_any_call(self.remark_lines[12:-2])



class AssemblyLinesToAssemblyDictTests(TestCase):

    def test_can_parse_simple_assembly(self):
        d = assembly_lines_to_assembly_dict([
         " 350 BIOMOLECULE: 1",
         " 350 SOFTWARE DETERMINED QUATERNARY STRUCTURE: DIMERIC",
         " 350 SOFTWARE USED: PISA",
         " 350 TOTAL BURIED SURFACE AREA: 1650 ANGSTROM**2",
         " 350 SURFACE AREA OF THE COMPLEX: 4240 ANGSTROM**2",
         " 350 CHANGE IN SOLVENT FREE ENERGY: -7.0 KCAL/MOL",
         " 350 APPLY THE FOLLOWING TO CHAINS: G, H",
         " 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         " 350   BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
         " 350   BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
         " 350"
        ])
        self.assertEqual(d, {
         "id": 1, "software": "PISA", "delta_energy": -7.0,
         "buried_surface_area": 1650.0, "surface_area": 4240.0,
         "transformations": [{
          "chains": ["G", "H"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 2.0, -6.0]
         }]
        })


    def test_can_parse_complex_assembly(self):
        d = assembly_lines_to_assembly_dict([
         " 350 BIOMOLECULE: 5",
         " 350 SOFTWARE DETERMINED QUATERNARY STRUCTURE: DODECAMERIC",
         " 350 SOFTWARE USED: PISA",
         " 350 TOTAL BURIED SURFACE AREA: 21680 ANGSTROM**2",
         " 350 SURFACE AREA OF THE COMPLEX: 12240 ANGSTROM**2",
         " 350 CHANGE IN SOLVENT FREE ENERGY: -332.0 KCAL/MOL",
         " 350 APPLY THE FOLLOWING TO CHAINS: E, F, G, H,",
         " 350                    AND CHAINS: J, K, L",
         " 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         " 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000",
         " 350   BIOMT3   1  0.000000  0.000000  1.000000        0.00000",
         " 350   BIOMT1   2 -0.500000 -0.866025  0.000000        0.00000",
         " 350   BIOMT2   2  0.866025 -0.500000  0.000000        0.00000",
         " 350   BIOMT3   2  0.000000  0.000000  1.000000        0.00000",
        ])
        self.assertEqual(d, {
         "id": 5, "software": "PISA", "delta_energy": -332.0,
         "buried_surface_area": 21680.0, "surface_area": 12240.0,
         "transformations": [{
          "chains": ["E", "F", "G", "H", "J", "K", "L"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "J", "K", "L"],
          "matrix": [[-0.5, -0.866025, 0.0], [0.866025, -0.5, 0.0], [0, 0, 1]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })


    def test_can_parse_sparse_assembly(self):
        d = assembly_lines_to_assembly_dict([
         " 350 BIOMOLECULE: 1",
         " 350 APPLY THE FOLLOWING TO CHAINS: G, H",
         " 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000",
         " 350   BIOMT2   1  0.000000  1.000000  0.000000        2.00000",
         " 350   BIOMT3   1  0.000000  0.000000  1.000000        -6.00000",
         " 350"
        ])
        self.assertEqual(d, {
         "id": 1, "software": None, "delta_energy": None,
         "buried_surface_area": None, "surface_area": None,
         "transformations": [{
          "chains": ["G", "H"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 2.0, -6.0]
         }]
        })



class AtomLineToAtomDictTests(TestCase):

    def test_can_convert_empty_line_to_atom(self):
        d = deepcopy(ATOM_DICT)
        d["polymer"] = True
        atom = atom_line_to_atom_dict(" " * 74)
        self.assertEqual(atom, d)


    def test_can_convert_full_line_to_atom(self):
        atom = atom_line_to_atom_dict(
         "  107  N1 AGLY B  13C     " +
         "12.681  37.302 -25.211 0.70  15.56           N2-"
        )
        self.assertEqual(atom, {
         "id": 107, "name": "N1",
         "alt_loc": "A", "residue_name": "GLY",
         "chain_id": "B", "residue_id": 13, "residue_insert": "C",
         "x": 12.681, "y": 37.302, "z": -25.211,
         "occupancy": 0.7, "bfactor": 15.56, "anisotropy": [],
         "element": "N", "charge": -2, "polymer": True, "full_res_id": "B13C"
        })


    def test_can_handle_numeric_residue_names(self):
        atom = atom_line_to_atom_dict(
         "  107  N1 A062 B  13C     " +
         "12.681  37.302 -25.211 0.70  15.56           N-2", polymer=False
        )
        self.assertEqual(atom["residue_name"], "062")
        self.assertFalse(atom["polymer"])



class AnisouAssingingTests(TestCase):

    def test_can_assign_anisou(self):
        model = {"atoms": [{"id": 107}, {"id": 108}, {"id": 109}, {"id": 110}]}
        models = [deepcopy(model), deepcopy(model)]
        assign_anisou({"ANISOU": [
         "  107  N   GLY A  13     2406   1892   1614    198    519   -328",
         "  110  O   GLY A  13     3837   2505   1611    164   -121    189"
        ]}, models)
        for model in models:
            self.assertEqual(model["atoms"], [
             {"id": 107, "anisotropy": [0.2406, 0.1892, 0.1614, 0.0198, 0.0519, -0.0328]},
             {"id": 108, "anisotropy": [0, 0, 0, 0, 0, 0]},
             {"id": 109, "anisotropy": [0, 0, 0, 0, 0, 0]},
             {"id": 110, "anisotropy": [0.3837, 0.2505, 0.1611, 0.0164, -0.0121, 0.0189]}
            ])



class SequenceExtractionTests(TestCase):

    def setUp(self):
        model = {"chains": [{
         "id": "C", "full_sequence": []}, {"id": "D", "full_sequence": []
        }]}
        self.models = [deepcopy(model), deepcopy(model)]


    def test_empty_sequence_extraction(self):
        m = deepcopy(self.models)
        extract_sequence({"HEADER": ["1"]}, m)
        self.assertEqual(m, self.models)


    @patch("atomium.files.pdb.merge_lines")
    def test_sequence_extraction(self, mock_merge):
        mock_merge.return_value = "C 15 JHY FRT C 15 FDR D YTR"
        extract_sequence({"SEQRES": ["line1", "line2"]}, self.models)
        for model in self.models:
            self.assertEqual(model["chains"], [
             {"id": "C", "full_sequence": ["JHY", "FRT", "FDR"]},
             {"id": "D", "full_sequence": ["YTR"]}
            ])



class ConnectionExtractionTests(TestCase):

    def test_empty_connection_extraction(self):
        models = [{"connections": []}, {"connections": []}]
        extract_connections({"HEADER": ["1"]}, models)
        self.assertEqual(models, [{"connections": []}, {"connections": []}])


    def test_extract_connections(self):
        models = [{"connections": []}, {"connections": []}]
        conect_lines = [
         " 1179  746 1184 1195 1203".ljust(74),
         " 1179 1211 1222".ljust(74),
         " 1221  544 1017 1020 1022".ljust(74)
        ]
        extract_connections({"CONECT": [
         " 1179  746 1184 1195 1203".ljust(74),
         " 1179 1211 1222".ljust(74),
         " 1221  544 1017 1020 1022".ljust(74)
        ]}, models)
        for model in models:
            self.assertEqual(model["connections"], [
             {"atom": 1179, "bond_to": [746, 1184, 1195, 1203, 1211, 1222]},
             {"atom": 1221, "bond_to": [544, 1017, 1020, 1022]}
            ])



class LineMergingTests(TestCase):

    def setUp(self):
        self.lines = ["0123456789 ", "abcdefghij ", "0123456789 "]
        self.punc_lines = ["0123, 456789 ", "abcd  efghij ", "0123; 456789 "]


    def test_can_merge_lines(self):
        self.assertEqual(
         merge_lines(self.lines, 5),
         "56789 fghij 56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8),
         "89 ij 89"
        )


    def test_can_vary_join(self):
        self.assertEqual(
         merge_lines(self.lines, 5, join=""),
         "56789fghij56789"
        )
        self.assertEqual(
         merge_lines(self.lines, 8, join="."),
         "89.ij.89"
        )
