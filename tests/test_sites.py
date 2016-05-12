from unittest import TestCase
from molecupy import exceptions
from molecupy.molecules import Atom, Molecule
from molecupy.macromolecules import Residue, ResiduicStructure, Site, MacroModel

class SiteTest(TestCase):

    def setUp(self):
        self.atom1 = Atom(1.0, 1.0, 1.0, "H", atom_id=1, atom_name="H1")
        self.atom2 = Atom(1.0, 1.0, 2.0, "C", atom_id=2, atom_name="CA")
        self.atom3 = Atom(1.0, 1.0, 3.0, "O", atom_id=3, atom_name="OX1")
        self.atom2.covalent_bond_to(self.atom1)
        self.atom2.covalent_bond_to(self.atom3)
        self.residue1 = Residue(1, "MON1", self.atom1, self.atom2, self.atom3)
        self.atom4 = Atom(1.0, 1.0, 4.0, "H", atom_id=4, atom_name="H1")
        self.atom5 = Atom(1.0, 1.0, 5.0, "C", atom_id=5, atom_name="CA")
        self.atom6 = Atom(1.0, 1.0, 6.0, "O", atom_id=6, atom_name="OX1")
        self.atom5.covalent_bond_to(self.atom4)
        self.atom5.covalent_bond_to(self.atom6)
        self.residue2 = Residue(2, "MON2", self.atom4, self.atom5, self.atom6)
        self.atom7 = Atom(1.0, 1.0, 7.0, "H", atom_id=7, atom_name="H1")
        self.atom8 = Atom(1.0, 1.0, 8.0, "C", atom_id=8, atom_name="CA")
        self.atom9 = Atom(1.0, 1.0, 9.0, "O", atom_id=9, atom_name="OX1")
        self.atom8.covalent_bond_to(self.atom7)
        self.atom8.covalent_bond_to(self.atom9)
        self.residue3 = Residue(3, "MON3", self.atom7, self.atom8, self.atom9)


    def check_valid_site(self, site):
        self.assertIsInstance(site, Site)
        self.assertIsInstance(site, ResiduicStructure)
        self.assertIsInstance(site.residues, set)
        if site.site_id is not None:
            self.assertIsInstance(site.site_id, int)
        if site.site_name is not None:
            self.assertIsInstance(site.site_name, str)
        if site.model is not None:
            self.assertIsInstance(site.model, MacroModel)
        if site.ligand is not None:
            self.assertIsInstance(site.ligand, Molecule)
        self.assertRegex(
         str(site),
         r"<Site \((\d+) residues\)>"
        )



class SiteCreationTests(SiteTest):

    def test_can_create_site(self):
        site = Site(
         self.residue1,
         self.residue2,
         self.residue3
        )
        self.check_valid_site(site)


    def test_can_create_site_with_id(self):
        site = Site(
         self.residue1,
         self.residue2,
         self.residue3,
         site_id=1
        )
        self.check_valid_site(site)


    def test_site_id_must_be_int(self):
        with self.assertRaises(TypeError):
            site = Site(
             self.residue1,
             self.residue2,
             self.residue3,
             site_id=1.1
            )
        with self.assertRaises(TypeError):
            site = Site(
             self.residue1,
             self.residue2,
             self.residue3,
             site_id="10"
            )


    def test_can_create_site_with_name(self):
        site = Site(
         self.residue1,
         self.residue2,
         self.residue3,
         site_name="AB1"
        )
        self.check_valid_site(site)


    def test_site_name_must_be_str(self):
        with self.assertRaises(TypeError):
            site = Site(
             self.residue1,
             self.residue2,
             self.residue3,
             site_name=1
            )



class SiteLigandTests(SiteTest):

    def test_can_add_ligand(self):
        site = Site(
         self.residue1,
         self.residue2,
         self.residue3
        )
        molecule = Molecule(Atom(1.0, 1.0, 1.0, "H"))
        site.molecule = molecule
        self.check_valid_site(site)