from abc import ABC, abstractmethod
import unittest
import itertools 
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


class AUT:
    """ Abstract UnitTests class nesting abstract classes so they won't be
    called during testing """


    class TestLogicConcept(ABC, unittest.TestCase):
        pass


    class TestFunction(TestLogicConcept, ABC): 
        @property
        @abstractmethod
        def cls_tested(self):
            raise NotImplementedError

        def setUp(self):
            self.c  = Constant('georges')
            self.v  = Variable('X')
            self.f = self.cls_tested('parent_of', [self.c, self.v])

        def test_attributes_and_str(self):
            self.assertEqual(self.f.arity, 2)
            self.assertEqual(self.f.name, 'parent_of/2')
            self.assertEqual(str(self.f), 'parent_of(georges, X)')

        def test_iter(self):
            for t1, t2 in zip(self.f, [self.c, self.v]):
                self.assertEqual(t1, t2)
            
        def test_apply(self):
            subst = {self.v:self.c}
            def fun(expr):
                if expr in subst:
                    return subst[expr]
                else:
                    return expr
            self.assertEqual(self.f.apply(fun).arguments, [self.c, self.c])


    class TestAtom(TestLogicConcept, ABC):
        @abstractmethod
        def get_3_different_objects(self) -> tuple[Atom, Atom, Atom]:
            pass

        def test_hashable(self):
            obj1, obj2, obj3 = self.get_3_different_objects()
            s = set()
            self.assertFalse(obj1 in s)
            self.assertFalse(obj2 in s)
            self.assertFalse(obj3 in s)
            s.add(obj1)
            self.assertTrue(obj1 in s)
            self.assertFalse(obj2 in s)
            self.assertFalse(obj3 in s)
            s.add(obj2)
            self.assertTrue(obj1 in s)
            self.assertTrue(obj2 in s)
            self.assertFalse(obj3 in s)
            s.remove(obj1)
            self.assertFalse(obj1 in s)
            self.assertTrue(obj2 in s)
            self.assertFalse(obj3 in s)


    class TestTerm(TestLogicConcept, ABC):
        @abstractmethod
        def get_3_different_objects(self) -> tuple[Atom, Atom, Atom]:
            pass

        def test_hashable(self):
            obj1, obj2, obj3 = self.get_3_different_objects()
            s = set()
            self.assertFalse(obj1 in s)
            self.assertFalse(obj2 in s)
            self.assertFalse(obj3 in s)
            s.add(obj1)
            self.assertTrue(obj1 in s)
            self.assertFalse(obj2 in s)
            self.assertFalse(obj3 in s)
            s.add(obj2)
            self.assertTrue(obj1 in s)
            self.assertTrue(obj2 in s)
            self.assertFalse(obj3 in s)
            s.remove(obj1)
            self.assertFalse(obj1 in s)
            self.assertTrue(obj2 in s)
            self.assertFalse(obj3 in s)


class TestClause(AUT.TestLogicConcept):
    def setUp(self):
        self.p1, self.p2, self.p3 = TestPredicate().get_3_different_objects()
        self.clause = Clause(self.p1, [self.p2, self.p3])

    def test_attributes_and_str(self):
        self.assertEqual(self.clause.head, self.p1)
        self.assertIn(self.p3, self.clause.body)

    def test_apply(self):
        leafs = set()
        def fun(expr):
            leafs.add(expr)
        self.clause.apply(fun)
        leafs2 = set()
        def fun(expr):
            leafs2.add(expr)
        self.p1.apply(fun)
        self.p2.apply(fun)
        self.p3.apply(fun)
        self.assertEqual(leafs, leafs2)

    def test_hashable(self):
        s = set()
        self.assertNotIn(self.clause, s)
        s.add(self.clause)
        self.assertIn(self.clause, s)
        s.remove(self.clause)
        self.assertNotIn(self.clause, s)


class TestGoal(AUT.TestLogicConcept): 
    def setUp(self):
        self.p1, self.p2, self.p3 = TestPredicate().get_3_different_objects()
        self.goal = Goal([self.p1, self.p2, self.p3])

    def test_attributes_and_str(self):
        self.assertIn(self.p1, self.goal)
        self.assertIn(self.p3, self.goal)
        self.assertIn(str(self.p2), str(self.goal))
        
    def test_apply(self):
        leafs = set()
        def fun(expr):
            leafs.add(expr)
        self.goal.apply(fun)
        leafs2 = set()
        def fun(expr):
            leafs2.add(expr)
        self.p1.apply(fun)
        self.p2.apply(fun)
        self.p3.apply(fun)
        self.assertEqual(leafs, leafs2)


class TestNegation(AUT.TestLogicConcept): 
    def setUp(self):
        tg = TestGoal()
        tg.setUp()
        self.goal = tg.goal
        self.neg = Negation(self.goal)

    def test_attributes_and_str(self):
        self.assertEqual(self.neg.goal, self.goal)
        self.assertIn(str(self.goal), str(self.neg))

    def test_apply(self):
        def return_leafs(obj):
            leafs = set()
            def fun(expr):
                leafs.add(expr)
            obj.apply(fun)
            return leafs
        self.assertEqual(return_leafs(self.neg), return_leafs(self.goal))


class TestPredicate(AUT.TestFunction, AUT.TestAtom):
    cls_tested = Predicate
    def get_3_different_objects(self):
        output = []
        for c, v in [('georges', 'X'), ('aa', 'Y'), ('georges', 'Y')]:
            c = Constant(c)
            v = Variable(v)
            output.append(self.cls_tested('parent_of', [c, v]))
        return output


class TestCompoundTerm(AUT.TestFunction, AUT.TestTerm):
    cls_tested = CompoundTerm
    def get_3_different_objects(self):
        output = []
        for c, v in [('georges', 'X'), ('aa', 'Y'), ('georges', 'Y')]:
            c = Constant(c)
            v = Variable(v)
            output.append(self.cls_tested('parent_of', [c, v]))
        return output


class TestConstant(AUT.TestAtom):
    def get_3_different_objects(self):
        return [Constant(c) for c in ['jacques', 4, 2.5]]

    def test_attributes_and_str(self):
        for s in ('jacques', 4, 2.5):
            c = Constant(s)
            self.assertEqual(c.value, s)
            self.assertEqual(str(c),str(s))
        for s in ([1, 2, 3], 'Jacques'):
            self.assertRaises(Exception, Constant, s)

    def test_to_variable_name(self):
        """ Tests that the output of to_variable_name can indeed be passed to 
        a variable as name """
        for s in ('jacques', 4, 2.5):
            c = Constant(s)
            Variable(c.to_variable_name())
            
    def test_apply(self):
        def fun(c):
            return c.value
        for s in ('jacques', 4, 2.5):
            c = Constant(s)
            self.assertEqual(c.apply(fun), c.value)

    def test_evaluate(self):
        for s in ('jacques', 4, 2.5):
            c = Constant(s)
            self.assertEqual(c.evaluate({}), s)
        

class TestVariable(AUT.TestAtom):
    def get_3_different_objects(self):
        return [Variable(v) for v in ('V','X','T')]

    def test_attributes_and_str(self):
        for symbol, tally_id in [('A', 1), ('Bar', 12)]:
            v = Variable(symbol, tally_id=tally_id)
            self.assertEqual(v.symbol, symbol)
            self.assertEqual(v.tally_id, tally_id)
            s = str(v)
            self.assertIsInstance(s,str)
            self.assertTrue(s[0].isupper()) 

    def test_is_in(self):
        v = Variable('V')
        expr_list = [
            Constant('cV'),
            Predicate('a', [Constant('cV'), Type('+', 'person')]),
        ]
        for expr in expr_list:
            self.assertFalse(v.is_in(expr))

        expr_list = [
            Variable('V'),
            Predicate('a', [Constant('c'), Variable('V')]),
        ]
        for expr in expr_list:
            self.assertTrue(v.is_in(expr))

    def test_apply(self):
        def fun(v):
            return [v, v]
        v = Variable('V')
        self.assertEqual(v.apply(fun), [v, v])

    def test_evaluate(self):
        v = Variable('V')
        self.assertEqual(v.evaluate({Variable('V'):4}), 4)
        self.assertRaises(Exception, v.evaluate, {Variable('V', tally_id=2):4})


class TestType(AUT.TestAtom):
    def get_3_different_objects(self):
        return [Type(sign, name) for sign, name in (('+', 'x'), ('#', 'x'), ('+', 'v'))]

    def test_attributes_and_str(self):
        for sign, name in itertools.product(['+', '-', '#'], ['person', 'a']):
            t = Type(sign, name)
            self.assertEqual(t.sign, sign)
            self.assertEqual(t.name, name)
            self.assertEqual(str(t), sign+name)
        self.assertRaises(Exception, Type, '_', 'person')
        self.assertRaises(Exception, Type, '+', 12)

    def test_apply(self):
        t = Type('+', 'person')
        fun = lambda x: str(x)
        self.assertEqual(t.apply(fun), '+person')


class TestList(AUT.TestAtom):
    def get_3_different_objects(self):
        return self.l1, self.l2, self.l3

    def setUp(self):
        self.c1, self.c2, self.c3 = TestConstant().get_3_different_objects()
        self.v1, self.v2, self.v3 = TestVariable().get_3_different_objects()
        self.l1 = List([self.c1, self.c2, self.c3]) 
        self.l2 = List([self.v1, self.v2], self.l1)
        self.l3 = List([self.c1, self.v1, self.c3])

    def test_apply(self):
        elements = set()
        def fun(expr):
            elements.add(expr)
        self.l1.apply(fun)


if __name__ == '__main__':
    unittest.main()
