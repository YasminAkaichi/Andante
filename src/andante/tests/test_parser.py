import unittest
from andante.parser import Parser
from andante.logic_concepts import (
    LogicConcept, 
    Clause, 
    Goal, 
    Negation, 
    Function, 
    Atom, 
    Term, 
    Predicate, 
    CompoundTerm, 
    Constant, 
    Variable, 
    Type, 
    List 
)
from andante.mode import (
    ModeCollection,
    Modeh,
    Modeb,
)
from andante.mathematical_expressions import (
    Comparison,
    ArithmeticComparison,
    UnificationComparison,
    ArithmeticExpression,
    TrigoExpression
)
from andante.program import AndanteProgram


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

            #-----------------------------------------------------#
            #                   Basic grammar                     #
            #-----------------------------------------------------#
    
    def test_variable(self):
        v = self.parser.parse('V', rule='variable')
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.symbol, 'V')
        self.assertEqual(v.tally_id, 0)
        self.assertRaises(Exception, self.parser.parse, 'y', rule='variable')

    def test_constant(self):
        c = self.parser.parse('fred', rule='constant')
        self.assertIsInstance(c, Constant)
        self.assertEqual(c.value, 'fred')
        self.assertEqual(self.parser.parse('12', rule='constant').value, 12)
        self.assertEqual(self.parser.parse('.5', rule='constant').value, .5)
        self.assertRaises(Exception, self.parser.parse, 'V', rule='constant')


            #-----------------------------------------------------#
            #                   Tests wrt files                   #
            #-----------------------------------------------------#
            
    def test_andantefile(self):
        s = """
        set(verbose,0).
        :-begin_bg.
        mortal(X) :- man(X).
        man(socrates).
        :-end_bg.
        """
        af = self.parser.parse(s, rule='andantefile')
        self.assertIsInstance(af, AndanteProgram)
        answer, _ = af.query("mortal(socrates).")
        self.assertTrue(answer)

    def test_pos_ex(self):
        s = """
        :- begin_in_pos. 
        man(pierre). man(socrates). 
        man(yves). mortal(X) :- man(X).
        :- end_in_pos.
        """
        ex = self.parser.parse(s, rule='pos_ex')
        self.assertEqual(len(ex), 4)

    def test_neg_ex(self):
        s = """
        :- begin_in_neg. 
        man(pierre). man(socrates). 
        man(yves). mortal(X) :- man(X).
        :- end_in_neg.
        """
        ex = self.parser.parse(s, rule='neg_ex')
        self.assertEqual(len(ex), 4)

    def test_determination(self):
        s = "determination(grandfather/2, grandparent/2)."
        dh, ldb = self.parser.parse(s, rule='determination')
        self.assertEqual(dh, 'grandfather/2')
        self.assertEqual(ldb[0], 'grandparent/2')
        self.assertEqual(len(ldb), 1)

    def test_set(self):
        s = "set(verbose,0)."
        opt, value = self.parser.parse(s, rule='set')
        self.assertEqual(opt, 'verbose')
        self.assertEqual(value, 0)


            #-----------------------------------------------------#
            #                Tests wrt horn clauses               #
            #-----------------------------------------------------#
    
    def test_hornclause(self):
        s = "parent_of ( georges , lucas )."
        c = self.parser.parse(s, rule='hornclause')
        self.assertIsInstance(c, Clause)
        self.assertEqual(len(c.body), 0)
        self.assertEqual(str(c.head).replace(' ',''), 'parent_of(georges,lucas)')

        s = "father(A, B) :- parent_of(A, B), male(A )."
        c = self.parser.parse(s, rule='hornclause')
        p = c.body[1]
        self.assertIsInstance(p, Predicate)
        self.assertEqual(str(p).strip(), 'male(A)')

        s = ":- male(A), female(A)."
        c = self.parser.parse(s, rule='hornclause')
        self.assertIsNone(c.head)

        s = "father(A, B) :-"
        self.assertRaises(Exception, self.parser.parse, s, rule='hornclause')

        s = "father(A, B) :- parent_of(A, B), male(A )"
        self.assertRaises(Exception, self.parser.parse, s, rule='hornclause')
        
    def test_atom(self):
        strings = [
            "true",
            "false",
            "parent_of ( georges , lucas )",
        ]
        for s in strings:
            self.parser.parse(s, rule='atom')

    def test_predicate(self):
        s = "parent_of ( georges , lucas )"
        p = self.parser.parse(s, rule='predicate')
        self.assertIsInstance(p, Predicate)
        self.assertEqual(len(p.arguments), 2)
        self.assertEqual(p.symbol, 'parent_of')

    def test_term(self):
        s = [
            "parent_of ( georges , lucas )",
            "georges",
            "V",
        ]
        self.assertIsInstance(self.parser.parse(s[0], rule='term'), CompoundTerm)
        self.assertIsInstance(self.parser.parse(s[1], rule='term'), Constant)
        self.assertIsInstance(self.parser.parse(s[2], rule='term'), Variable)

    def test_compoundterm(self):
        s = "parent_of ( georges , lucas )"
        cp = self.parser.parse(s, rule='compoundterm')
        self.assertIsInstance(cp, CompoundTerm)
        self.assertEqual(len(cp.arguments), 2)
        self.assertEqual(cp.symbol, 'parent_of')

    def test_list(self):
        s = "[a, b, c | [a, b, c, d]]"
        l = self.parser.parse(s, rule='list')
        self.assertEqual(len(l.elements1), 3)
        self.assertIsInstance(l.elements2, List)
        self.assertEqual(len(l.elements2.elements1), 4)


            #-----------------------------------------------------#
            #                   Tests wrt modes                   #
            #-----------------------------------------------------#

    def test_modeh(self):
        s = "modeh(*, parent_of(+person, -person))."
        m = self.parser.parse(s, rule='mode')
        self.assertIsInstance(m, Modeh)

    def test_modeb(self):
        s = "modeb(*, parent_of(+person, -person))."
        m = self.parser.parse(s, rule='mode')
        self.assertIsInstance(m, Modeb)

    def test_recall(self):
        self.assertEqual(self.parser.parse('5', rule='recall'), 5)
        self.assertIsInstance(self.parser.parse('*', rule='recall'), int)

    def test_type(self):
        s = '+person'
        t = self.parser.parse(s, rule='type')
        self.assertIsInstance(t, Type)
        self.assertEqual(t.sign, '+')
        self.assertEqual(t.name, 'person')

    def test_sign(self):
        self.assertEqual('#', self.parser.parse('#', rule='sign'))
        self.assertEqual('+', self.parser.parse('+', rule='sign'))
        self.assertRaises(Exception, self.parser.parse, '+person', rule='sign')


            #-----------------------------------------------------#
            #                  Tests wrt queries                  #
            #-----------------------------------------------------#
    
    def test_query(self):
        s = "not(p1(V), p2(B)), p3(V,B)."
        q = self.parser.parse(s, rule="query")
        self.assertIsInstance(q, Goal)
        self.assertRaises(Exception, self.parser.parse, "not(p1(V), p2(B)), p3(V,B)", rule='query')

    def test_goal(self):
        s = "not(p1(V), p2(B)), p3(V,B)"
        g = self.parser.parse(s, rule="goal")
        self.assertIsInstance(g, Goal)

    def test_negation(self):
        s = "not(p1(V), p2(B))"
        n = self.parser.parse(s, rule="negation")
        self.assertIsInstance(n, Negation)


            #-----------------------------------------------------#
            #         Tests wrt parse_several method              #
            #-----------------------------------------------------#

    def test_parse_several(self):
        s = "man(georges). man(peter). man(victor)."
        clauses = self.parser.parse_several(s, rule='hornclause')
        for c in clauses:
            self.assertIsInstance(c, Clause)


if __name__=='__main__':
    unittest.main()
