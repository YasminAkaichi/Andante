from abc import ABC, abstractmethod

from aloe.options import Options
from aloe.clause  import Atom, Clause
from aloe.clausecollection import TreeBasedClauseCollection

from collections.abc import Iterable

class Knowledge(ABC):
    @abstractmethod
    def match(self, atom):
        pass
    
    @abstractmethod
    def add(self, clause):
        pass
    
    @abstractmethod
    def remove(self, clause):
        pass
    
    @abstractmethod
    def copy(self):
        pass

class MultipleKnowledge(Knowledge):
    def __init__(self, *knowledges, options=None):
        assert len(knowledges) >= 1
        self.options = options if options is not None else Options()
        self.knowledges = knowledges
        
    @property
    def clauses(self):
        return [c for k in self.knowledges for c in k.clauses]
        
    def match(self, atom):
        x = [k.match(atom) for k in self.knowledges]
        return set.union(*x)
    
    def add(self, x):
        if   isinstance(x, Knowledge):
            self.knowledges.append(x)
        else:
            self.knowledges[0].add(x)
    
    def remove(self, x):
        for k in self.knowledges:
            k.remove(x)
    
    def __repr__(self):
        tab = ' '*3
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
    
    def add(self, x):
        assert isinstance(x, (Clause, Knowledge, Iterable))
        if   isinstance(x, Clause):
            assert isinstance(x, Clause)
            self.clauses.append(x)
            self.collection.add(x)
        elif isinstance(x, Knowledge):
            for c in x.clauses:
                self.add(c)
        else:# isinstance(x, Iterable):
            for c in x:
                self.add(c)
        
    def remove(self, x):
        assert isinstance(x, (Iterable, Clause))
        if isinstance(x, Clause):
            x = [x]            
        x_ = set(x)
        self.clauses = [c for c in self.clauses if c not in x_]
        for c in x:
            self.collection.remove(c)
        
    def __repr__(self):
        tab = '   '
        tab_repr = [tab+repr(c).replace('\n','\n'+tab) for c in self.clauses]
        return 'LogicProgram object\n'+'\n'.join(tab_repr)

    def copy(self):
        return LogicProgram(self.clauses, self.options)