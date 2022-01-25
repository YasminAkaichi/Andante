from abc import ABC, abstractmethod

class Clause:
    def __init__(self, head, body):
        self.head = head
        self.body = body
                
    def __repr__(self):
        head_repr = repr(self.head)
        body_repr = ','.join([repr(term) for term in self.body])
        if not self.body:
            return '%s.' % (head_repr)
        elif self.head:
            return '%s:-%s.' % (head_repr, body_repr)
        else:
            return ':-%s.' % (body_repr)
        
    def __hash__(self):
        return hash(str(self))
        
    def __eq__(self, other):
        return str(self)==str(other)
    
    def is_unit(self):
        n_atoms = (1 if self.head else 0) + len(self.body)
        return n_atoms==1
    
    def is_skomelized(self):
        return (self.head.is_skomelized() if self.head else True) and all([atom.is_skomelized() for atom in self.body])

class Operator(ABC):
    def __init__(self, name, terms):
        self._name = name
        self.terms = terms
        
    @property
    def name(self): return self._name
    @property 
    def longname(self): return '%s/%d' % (self.name,self.arity)
    @property
    def arity(self): return len(self.terms)
    
    def __iter__(self): return iter(self.terms)    
    def __repr__(self): return '%s(%s)' % (self.name, ','.join([repr(term) for term in self.terms]))
    
    def is_skolemized(self):
        return all([term.is_skomelized() for term in self])
    
class Atom(ABC):
    pass

class Term(ABC):
    def __hash__(self):      return hash(repr(self))
    def __eq__(self, other): return repr(self) == repr(other)

class Predicate(Atom, Operator):
    pass
        
class Function(Term, Operator):
    pass
    
class Constant(Term):
    def __init__(self, value):
        self.value = value
        
    def __repr__(self): return str(self.value)
    def is_skolemized(self): return True
    
class Variable(Term):
    def __init__(self, value):
        """ 
        A variable is represented by a single value.
        This value can be a string (Ex: 'Animal') or a number (Ex: 12)
        """
        self.value = value
        
    def __repr__(self): return 'V%d' % (self.value) if isinstance(self.value, int) else self.value
    def is_skolemized(self): return False
    
