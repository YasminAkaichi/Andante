from aloe.clause  import *
from aloe.options import *
from aloe.mode    import ModeHandler
from aloe.parser  import AloeParser
from aloe.solver  import AloeSolver
from aloe.clausecollection import TreeBasedClauseCollection

class AloeProgram:
    def __init__(self, B=None, E=None, M=None, options=DefaultOptions()):
        """
        Class representing a Aloe program
        Attributes:
            -B: background knowledge
            -E: examples
            -M: modes
            -options: options
        """
        self.B = B if B else LogicProgram()
        self.E = E if E else {'pos':[], 'neg':[]}
        self.M = M if M else Modehandler()
        self.options = options
        self.parser = AloeParser()
        self.solver = AloeSolver(self, self)
        
    def __repr__(self):
        B = repr(self.B)
        E = repr(self.E)
        M = repr(self.M)
        o = repr(self.options)
        return 'Background:\n%s\n\nExamples:\n%s\n\nModes:\n%s\n\noptions:\n%s' % (B,E,M,o)
    
    def query(self, q):
        """
        Launch a query to the aloe program. 
        The query 'q' can be:
        - a string: the query will then first be parsed and then evaluated
        - a clause
        - a list of clauses
        """
        if isinstance(q, str):
            q = list(self.parser.parse_clauses(q))            
        return self.solver.query(q)
        
class LogicProgram:
    def __init__(self, clauses=None):
        self.clauses = clauses if clauses else list()
        self.collection = TreeBasedClauseCollection(self.clauses)
        
    def match(self, atom):
        return self.collection.match(atom)
        
    def __repr__(self):
        return '\n'.join([str(clause) for clause in self.clauses])

  