from unittest import TestCase
from unittest.mock import patch, Mock
from atomium.structures.atoms import Atom, Bond

class AtomCreationTests(TestCase):

    def test_can_create_atom(self):
        atom = Atom("C", 2, 3, 5)
        self.assertEqual(atom._element, "C")
        self.assertEqual(atom._x, 2)
        self.assertEqual(atom._y, 3)
        self.assertEqual(atom._z, 5)
        self.assertEqual(atom._id, None)
        self.assertEqual(atom._name, None)
        self.assertEqual(atom._charge, 0)
        self.assertEqual(atom._bonds, set())


    def test_atom_element_must_be_str(self):
        with self.assertRaises(TypeError):
            Atom(1, 2, 3, 5)


    def test_atom_element_must_be_1_or_2_chars(self):
        with self.assertRaises(ValueError):
            Atom("", 2, 3, 5)
        with self.assertRaises(ValueError):
            Atom("XXX", 2, 3, 5)
        Atom("XX", 2, 3, 5)
        Atom("X", 2, 3, 5)


    def test_atom_x_coord_must_be_number(self):
        with self.assertRaises(TypeError):
            Atom("C", "2", 3, 5)
        Atom("C", 2.5, 3, 5)


    def test_atom_y_coord_must_be_number(self):
        with self.assertRaises(TypeError):
            Atom("C", 2, "3", 5)
        Atom("C", 2, 3.5, 5)


    def test_atom_z_coord_must_be_number(self):
        with self.assertRaises(TypeError):
            Atom("C", 2, 3, "5")
        Atom("C", 2, 3, 5.5)


    def test_can_create_atom_with_id(self):
        atom = Atom("C", 2, 3, 5, atom_id=20)
        self.assertEqual(atom._id, 20)


    def test_atom_id_must_be_integer(self):
        with self.assertRaises(TypeError):
            Atom("C", 2, 3, 5, atom_id=20.5)


    def test_atom_id_must_be_unique(self):
        atom = Atom("C", 2, 3, 5, atom_id=21)
        with self.assertRaises(ValueError):
            Atom("D", 5, 1, 6.5, atom_id=21)


    def test_can_create_atom_with_name(self):
        atom = Atom("C", 2, 3, 5, name="CA")
        self.assertEqual(atom._name, "CA")


    def test_atom_name_must_be_str(self):
        with self.assertRaises(TypeError):
            Atom("C", 2, 3, 5, name=20.5)


    def test_can_create_atom_with_charge(self):
        atom = Atom("C", 2, 3, 5, charge=-2.5)
        self.assertEqual(atom._charge, -2.5)


    def test_atom_charge_must_be_number(self):
        with self.assertRaises(TypeError):
            Atom("C", 2, 3, 5, charge="20.5")
        Atom("C", 2, 3, 5, charge=10)



class AtomReprTests(TestCase):

    def test_atom_repr(self):
        atom = Atom("C", 2, 3, 5)
        self.assertEqual(str(atom), "<C Atom at (2, 3, 5)>")



class AtomIdChangesTests(TestCase):

    def test_changing_id_updates_known_ids(self):
        atom = Atom("C", 2, 3, 5, atom_id=30)
        self.assertIn(30, Atom.known_ids)
        atom._id = 31
        self.assertIn(31, Atom.known_ids)
        self.assertNotIn(30, Atom.known_ids)


    def test_deleting_an_atom_frees_up_its_id(self):
        atom = Atom("C", 2, 3, 5, atom_id=40)
        self.assertIn(40, Atom.known_ids)
        atom = Atom("C", 2, 3, 5, atom_id=41)
        self.assertNotIn(40, Atom.known_ids)
        self.assertIn(41, Atom.known_ids)



class AtomElementTests(TestCase):

    def test_element_property(self):
        atom = Atom("C", 2, 3, 5)
        self.assertIs(atom._element, atom.element())


    def test_can_update_element(self):
        atom = Atom("C", 2, 3, 5)
        atom.element("N")
        self.assertEqual(atom._element, "N")


    def test_atom_element_must_be_str(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom.element(1)


    def test_atom_element_must_be_1_or_2_chars(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(ValueError):
            atom.element("")
        with self.assertRaises(ValueError):
            atom.element("XXX")
        atom.element("XX")



class AtomXTests(TestCase):

    def test_x_property(self):
        atom = Atom("C", 2, 3, 5)
        self.assertIs(atom._x, atom.x())


    def test_can_update_x(self):
        atom = Atom("C", 2, 3, 5)
        atom.x(6)
        self.assertEqual(atom._x, 6)


    def test_atom_x_must_be_numeric(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom.x("4")
        atom.x(4.5)



class AtomYTests(TestCase):

    def test_y_property(self):
        atom = Atom("C", 2, 3, 5)
        self.assertIs(atom._y, atom.y())


    def test_can_update_y(self):
        atom = Atom("C", 2, 3, 5)
        atom.y(6)
        self.assertEqual(atom._y, 6)


    def test_atom_y_must_be_numeric(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom.y("4")
        atom.y(4.5)



class AtomZTests(TestCase):

    def test_z_property(self):
        atom = Atom("C", 2, 3, 5)
        self.assertIs(atom._z, atom.z())


    def test_can_update_z(self):
        atom = Atom("C", 2, 3, 5)
        atom.z(6)
        self.assertEqual(atom._z, 6)


    def test_atom_z_must_be_numeric(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom.z("4")
        atom.z(4.5)



class AtomIdTests(TestCase):

    def test_id_property(self):
        atom = Atom("C", 2, 3, 5, atom_id=100)
        self.assertIs(atom._id, atom.atom_id())


    def test_can_update_id(self):
        atom = Atom("C", 2, 3, 5, atom_id=101)
        atom.atom_id(102)
        self.assertEqual(atom._id, 102)


    def test_atom_id_must_be_numeric(self):
        atom = Atom("C", 2, 3, 5, atom_id=105)
        with self.assertRaises(TypeError):
            atom.atom_id("4")



class AtomNameTests(TestCase):

    def test_name_property(self):
        atom = Atom("C", 2, 3, 5, name="CA")
        self.assertIs(atom._name, atom.name())


    def test_can_update_name(self):
        atom = Atom("C", 2, 3, 5, name="CA")
        atom.name("CB")
        self.assertEqual(atom._name, "CB")


    def test_atom_name_must_be_str(self):
        atom = Atom("C", 2, 3, 5, name="CA")
        with self.assertRaises(TypeError):
            atom.name(4)



class AtomChargeTests(TestCase):

    def test_charge_property(self):
        atom = Atom("C", 2, 3, 5, charge=0.5)
        self.assertIs(atom._charge, atom.charge())


    def test_can_update_charge(self):
        atom = Atom("C", 2, 3, 5)
        atom.charge(6)
        self.assertEqual(atom._charge, 6)


    def test_atom_charge_must_be_numeric(self):
        atom = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom.charge("4")
        atom.charge(4.5)



class AtomBondsTests(TestCase):

    def test_bonds_property(self):
        atom = Atom("C", 2, 3, 5)
        atom._bonds = set(("bond1", "bond2"))
        self.assertEqual(atom.bonds(), atom._bonds)
        self.assertIsNot(atom.bonds(), atom._bonds)



class BondedAtomTests(TestCase):

    @patch("atomium.structures.atoms.Atom.bonds")
    def test_can_get_bonded_atoms(self, mock_bonds):
        atom = Atom("C", 2, 3, 5)
        bond1, bond2, bond3 = Mock(Bond), Mock(Bond), Mock(Bond)
        atom2, atom3, atom4 = Mock(Atom), Mock(Atom), Mock(Atom)
        bond1.atoms.return_value = set([atom, atom2])
        bond2.atoms.return_value = set([atom, atom3])
        bond3.atoms.return_value = set([atom, atom4])
        mock_bonds.return_value = set([bond1, bond2, bond3])
        self.assertEqual(atom.bonded_atoms(), set([atom2, atom3, atom4]))



class AtomBondingTests(TestCase):

    @patch("atomium.structures.atoms.Bond.__init__")
    def test_can_bond_other_atom(self, mock_bond):
        atom1 = Atom("C", 2, 3, 5)
        atom2 = Mock(Atom)
        mock_bond.return_value = None
        atom1.bond(atom2)
        mock_bond.assert_called_with(atom1, atom2)



class AtomBondBreakingTests(TestCase):

    @patch("atomium.structures.atoms.Atom.bonds")
    def test_can_break_bond_between_atoms(self, mock_bonds):
        atom1 = Atom("C", 2, 3, 5)
        atom2 = Mock(Atom)
        bond = Mock(Bond)
        bond.atoms.return_value = set([atom1, atom2])
        mock_bonds.return_value = set([bond])
        atom2.bonds.return_value = set([bond])
        atom1.unbond(atom2)
        bond.destroy.assert_called()


    def test_bond_breaking_needs_atoms(self):
        atom1 = Atom("C", 2, 3, 5)
        with self.assertRaises(TypeError):
            atom1.unbond("atom2")


    @patch("atomium.structures.atoms.Atom.bonds")
    def test_bond_unbreaking_needs_actual_bond(self, mock_bonds):
        atom1 = Atom("C", 2, 3, 5)
        atom2 = Mock(Atom)
        bond = Mock(Bond)
        bond.atoms.return_value = set([atom1, Mock(Atom)])
        mock_bonds.return_value = set([bond])
        atom2.bonds.return_value = set([bond])
        with self.assertRaises(ValueError):
            atom1.unbond(atom2)




class AtomMassTests(TestCase):

    def test_known_element_mass(self):
        atom = Atom("C", 2, 3, 5)
        self.assertAlmostEqual(atom.mass(), 12, delta=0.1)
        atom._element = "H"
        self.assertAlmostEqual(atom.mass(), 1, delta=0.1)


    def test_atom_mass_case_insensitive(self):
        atom = Atom("he", 2, 3, 5)
        self.assertAlmostEqual(atom.mass(), 4, delta=0.1)
        atom = Atom("He", 2, 3, 5)
        self.assertAlmostEqual(atom.mass(), 4, delta=0.1)
        atom = Atom("hE", 2, 3, 5)
        self.assertAlmostEqual(atom.mass(), 4, delta=0.1)
        atom = Atom("HE", 2, 3, 5)
        self.assertAlmostEqual(atom.mass(), 4, delta=0.1)


    def test_unknown_atom_mass(self):
        atom = Atom("XX", 2, 3, 5)
        self.assertEqual(atom.mass(), 0)



class AtomDistanceToTests(TestCase):

    def test_can_get_distance_between_atoms(self):
        atom1 = Atom("C", 4, 8, 3)
        atom2 = Atom("H", 2, 3, 5)
        self.assertAlmostEqual(atom1.distance_to(atom2), 5.744, delta=0.001)


    def test_atom_distance_can_be_zero(self):
        atom1 = Atom("C", 4, 8, 3)
        atom2 = Atom("H", 4, 8, 3)
        self.assertEqual(atom1.distance_to(atom2), 0)


    def test_other_atom_must_be_atom(self):
        atom1 = Atom("C", 4, 8, 3)
        atom2 = "atom"
        with self.assertRaises(TypeError):
            atom1.distance_to(atom2)


    def test_can_get_distance_to_xyz_tuple(self):
        atom1 = Atom("C", 4, 8, 3)
        atom2 = (2, 3, 5)
        self.assertAlmostEqual(atom1.distance_to(atom2), 5.744, delta=0.001)
