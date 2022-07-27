import unittest
from aloe.mode import Modeb, Modeh, ModeCollection
from aloe.logic_concepts import Constant, Predicate, Variable, Type

class TestMode(unittest.TestCase):
    """ Tests the Modeh and Modeb objects """
    def setUp(self):
        self.t  = Type('+', 'person')
        self.c  = Constant('father')
        self.a  = Predicate('kinship', [self.c, self.t, self.t])

    def test_attributes(self):
        """ Tests that Modeh and Modeb classes are well initialized """
        mh = Modeh(5, self.a) 
        mb = Modeb(5, self.a) 
        for m in (mh, mb):
            self.assertEqual(m.atom_arity, self.a.arity)
            self.assertEqual(m.atom_name, self.a.name)
            
    def test_mode_instantiation(self):
        """ Test the 'instantiate' method of the Modeh and Modeb classes """
        mh = Modeh(5, self.a) 
        mb = Modeb(5, self.a) 
        for m in (mh, mb):
            a = m.instantiate()
            self.assertEqual(a.symbol, self.a.symbol)
            c, v1, v2 = a.arguments
            self.assertEqual(c, self.c)
            self.assertIsInstance(v1, Variable)
            self.assertIsInstance(v2, Variable)
            self.assertNotEqual(v1, v2)
            
class TestModeCollection(unittest.TestCase):
    """ Tests the ModelCollection class """
    def setUp(self):
        self.t1 = Type('+', 'class1')
        self.t2 = Type('-', 'class1')
        self.m1 = Modeh(1, Predicate('fun1', [self.t1, self.t2]))
        self.m2 = Modeb(1, Predicate('fun1', [self.t1, self.t2]))
        self.m3 = Modeb(1, Predicate('fun2', [self.t1, self.t2]))
        self.m4 = Modeh(1, Predicate('fun3', [self.t1, self.t2]))
        self.m5 = Modeh(1, Predicate('fun4', [self.t1, self.t2]))
        self.m6 = Modeb(1, Predicate('fun5', [self.t1, self.t2]))
        self.modes = [self.m1, self.m2, self.m3, self.m4]
        self.determinations = [
            ('fun1/2', ['fun1/2', 'fun2/2']),
            ('fun3/2', ['fun2/2']),
        ]
        
    def test_get_mode(self):
        """ Tests all get methods (get_modeh, get_modeb and get_modeb_from_modeh) """
        M = ModeCollection(modes=self.modes, determinations=self.determinations)
        self.assertEqual(M.get_modeh(self.m1.atom_name), self.m1)
        self.assertEqual(M.get_modeb(self.m2.atom_name), self.m2)
        self.assertRaises(KeyError, M.get_modeh, self.m3.atom_name)
        self.assertRaises(KeyError, M.get_modeb, self.m4.atom_name)
        self.assertRaises(KeyError, M.get_modeb, self.m6.atom_name)
        self.assertRaises(KeyError, M.get_modeh, self.m5.atom_name)
        self.assertIn(self.m2, M.get_modeb_from_modeh(self.m1.atom_name))
        self.assertIn(self.m3, M.get_modeb_from_modeh(self.m1.atom_name))
        self.assertIn(self.m3, M.get_modeb_from_modeh(self.m4.atom_name))
        self.assertNotIn(self.m2, M.get_modeb_from_modeh(self.m4.atom_name))

    def test_add(self):
        """ Tests the add and get methods """
        M = ModeCollection(modes=self.modes, determinations=self.determinations)
        # Tests for Modeh
        M.add(self.m5)
        self.assertEqual(M.get_modeh(self.m5.atom_name), self.m5)
        M.remove(self.m5)
        self.assertRaises(KeyError, M.get_modeh, self.m5.atom_name)
        # Tests for Modeb
        M.add(self.m6)
        self.assertEqual(M.get_modeb(self.m6.atom_name), self.m6)
        M.remove(self.m6)
        self.assertRaises(KeyError, M.get_modeb, self.m6.atom_name)
        # Tests for determination
        deter = ('fun3/2', ['fun1/2'])
        M.add(deter)
        self.assertIn(self.m2, M.get_modeb_from_modeh(self.m4.atom_name))
        M.remove(deter)
        self.assertNotIn(self.m2, M.get_modeb_from_modeh(self.m4.atom_name))
        
if __name__ == "__main__":
    unittest.main()
