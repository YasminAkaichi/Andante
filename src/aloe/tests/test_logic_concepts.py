import unittest
from aloe.logic_concepts import (
    Clause, 
    Predicate, 
    CompoundTerm, 
    Constant, 
    Variable,
    Type,
    Goal,
    Negation,
    List,
)

class TestConstant(unittest.TestCase):
    def test_ok(self):
        for s in ('Jacques', 4):
            c = Constant(s)
            self.assertEqual(c.value, s)
            self.assertEqual(str(c),str(s))

class TestVariable(unittest.TestCase):
    pass

class TestType(unittest.TestCase):
    pass

class TestCompoundTerm(unittest.TestCase):
    pass

class TestPredicate(unittest.TestCase):
    pass

class TestClause(unittest.TestCase):
    pass

class TestGoal(unittest.TestCase):
    pass

class TestNegation(unittest.TestCase):
    pass

class TestList(unittest.TestCase):
    pass
