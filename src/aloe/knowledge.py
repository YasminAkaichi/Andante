from abc import ABC, abstractmethod

from aloe.options import Options
from aloe.clause  import Atom, Clause
from aloe.clausecollection import TreeBasedClauseCollection

class Knowledge(ABC):
    @abstractmethod
    def match(self, atom):
        pass
    
    @abstractmethod
    def add(self, clause):
        pass
    
    @abstractmethod
    def copy(self):
        pass

class MultipleKnowledge(Knowledge):
    def __init__(self, *knowledges, options=None):
        assert len(knowledges) >= 1
        self.options = options if options is not None else Options()
        self.knowledges = knowledges
        
    def match(self, atom):
        x = [k.match(atom) for k in self.knowledges]
        return set.union(*x)
    
    def add(self, clause):
        assert isinstance(clause, Clause)
        self.knowledges[0].add(clause, clause)
    
    def __repr__(self):
        tab = '   '
        tab_repr = [tab+repr(k).replace('\n','\n'+tab) for k in self.knowledges]
        return 'MultipleKnowledge object\n'+'\n\n'.join(tab_repr)
    
    def copy():
        return MultipleKnowledge(*[k.copy() for k in self.knowledges], self.options)
    
class LogicProgram(Knowledge):
    def __init__(self, clauses=None, options=None):
        self.options = options if options is not None else Options()
        self.clauses = clauses if clauses else list()
        self.collection = TreeBasedClauseCollection(self.clauses)
        
    def match(self, atom):
        assert isinstance(atom, Atom)
        return self.collection.match(atom)
    
    def add(self, clause):
        assert isinstance(clause, Clause)
        self.clauses.append(clause)
        self.collection.add(clause)
        
    def __repr__(self):
        tab = '   '
        tab_repr = [tab+repr(c).replace('\n','\n'+tab) for c in self.clauses]
        return 'LogicProgram object\n'+'\n'.join(tab_repr)

    def copy(self):
        return LogicProgram(self.clauses, self.options)