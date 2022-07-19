import unittest
from aloe.program import AloeProgram
from aloe.parser import Parser

s = """ 
% Contents of the file Examples/short_family.pl
modeh(*,daughter(+person,-person)).
modeb(*,parent(+person,-person)).
modeb(*,parent(-person,+person)).
modeb(*,female(+person)).
modeb(*,female(-person)).
%
determination(daughter/2,parent/2).
determination(daughter/2,female/1).
%    
set(verbose,1).

:- begin_bg.
person(ann).
person(mary).
person(tom).
person(eve).
person(lucy).

parent(ann,mary).
parent(ann,tom).
parent(tom,eve).
parent(tom,lucy).

female(ann).
female(mary).
female(eve).
female(lucy).
:- end_bg.
    

:- begin_in_pos.
daughter(lucy,tom).
daughter(mary,ann).
daughter(eve,tom).
:- end_in_pos.

:- begin_in_neg.
daughter(tom,ann).
daughter(tom,eve).
:- end_in_neg.
"""    
    
class TestAloeProgram(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.ap = AloeProgram.build_from(s)
    
    def test_build_from(self):
        ap = AloeProgram.build_from("Examples/short_family.pl")
        self.assertIsInstance(ap, AloeProgram)

    def test_build_from_background(self):
        bckg = """
        person(ann).
        person(mary).
        person(tom).
        person(eve).
        person(lucy).

        parent(ann,mary).
        parent(ann,tom).
        parent(tom,eve).
        parent(tom,lucy).

        female(ann).
        female(mary).
        female(eve).
        female(lucy).
        """
        ap = AloeProgram.build_from_background(bckg)
        self.assertIsInstance(ap, AloeProgram)
        self.assertEqual(len(ap.examples['pos']), 0)
        self.assertEqual(len(ap.examples['neg']), 0)
        a1 = self.parser.parse("person(eve)", rule='atom')
        a2 = self.parser.parse("person(john)", rule='atom')
        self.assertNotEqual(len(ap.match(a1)), 0)
        self.assertEqual(len(ap.match(a2)), 0)

    def test_query(self):
        ans, df = self.ap.query("parent(X,eve).")
        self.assertEqual(ans, True)
        self.assertEqual(df['X'], 'tom') 

        ans, _ = self.ap.query("parent(eve,X).")
        self.assertEqual(ans, False)

    def test_verify(self):
        pass

    def test_set(self):
        pass
    def test_induce(self):
        pass
    def test_generate_examples(self):
        pass
    def test_generate_examples_from_clause(self):
        pass
    

if __name__=='__main__':
    unittest.main()
