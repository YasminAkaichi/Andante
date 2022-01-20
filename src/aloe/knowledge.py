from abc import ABC, abstractmethod

from aloe.options import Options
from aloe.clause  import Atom, Clause
from aloe.clausecollection import TreeBasedClauseCollection

class Knowledge(ABC):
    @abstractmethod
    def match(self, atom):
        pass
    
class LogicProgram(Knowledge):
    def __init__(self, clauses=None, options=None):
        self.options = options if options is not None else Options()
        self.clauses = clauses if clauses else list()
        self.collection = TreeBasedClauseCollection(self.clauses)
        
    def match(self, atom):
        assert isinstance(atom, Atom)
        return self.collection.match(atom)
        
    def __repr__(self):
        return '\n'.join([str(clause) for clause in self.clauses])
    