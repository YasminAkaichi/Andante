from abc import ABC, abstractmethod
        
class Clause:
    def __init__(self, head, body):
        assert isinstance(head, Atom) or head is None
        assert isinstance(body, list) and all((isinstance(batom, Atom) for batom in body))
        self.head = head
        self.body = body
                
    def __repr__(self):
        head_repr = repr(self.head)
        body_repr = ','.join([repr(term) for term in self.body])
        if not self.body: return '%s.'     % (head_repr)
        elif self.head:   return '%s:-%s.' % (head_repr, body_repr)
        else:             return ':-%s.'   % (body_repr)
        
    def __hash__(self):
        return hash(str(self))
        
    def __eq__(self, other):
        return str(self)==str(other)
    
class Goal: 
    """ A goal is a list of literals """
    def __init__(self, literals):
        assert isinstance(literals, list) and all((isinstance(l, Literal) for l in literals))
        self.literals = literals
        
    def __iter__(self): return iter(self.literals)

class Literal:
    """ Represents a literal, that is a positive or a negative atom. """
    def __init__(self, atom, sign='+'):
        assert isinstance(atom, Atom) and sign in ('+','-')
        self.atom = atom
        self.sign = sign    
    
class Function(ABC):
    """ 
    Represents a function as the general form of a predicate and a CompoundTerm.
    Functions are composed of a functor and arguments.
    Arguments must be terms.
    """
    def __init__(self, functor, arguments):
        assert isinstance(functor, str)
        assert isinstance(arguments, (list,tuple)) and all((isinstance(arg, Term) for arg in arguments))
        self.functor   = functor
        self.arguments = arguments
        
    @property
    def name(self): return '%s/%d' % (self.functor,self.arity)
    @property
    def arity(self): return len(self.arguments)
    
    def __iter__(self): return iter(self.arguments)    
    def __repr__(self): return '%s(%s)' % (self.functor, ','.join([repr(arg) for arg in self.arguments]))

    
class Atom(ABC):
    """ Represents an atom in the first order logic framework """
    def __hash__(self):      return hash(repr(self))
    def __eq__(self, other): return repr(self) == repr(other)    
    
class Term(ABC):
    def __hash__(self):      return hash(repr(self))
    def __eq__(self, other): return repr(self) == repr(other)

class Predicate(Atom, Function): pass
        
class CompoundTerm(Term, Function):
    """ This class represents compound terms as defined in the prolog framework """
    pass
    
class Constant(Term):
    """ A constant is represented by its value that can be a int, float or a string """
    def __init__(self, value):
        assert isinstance(value, (int, float, str))
        self.value = value
        
    def __repr__(self): return str(self.value)
    
    def to_variable_name(self):
        """ Returns a valid unique variable name """
        if isinstance(self.value, str): return self.value.capitalize()
        else:                           return 'V' + str(self.value)
    
class Variable(Term):
    """ 
    This class represents variables in the first order logic framework
    Variable objects are distinguished by 
    - a symbol: a string (Ex: 'A', 'Father')
    - a tally id: a integer
    There can be several Variable objects with the same symbol. To distinguish among them, we use a tally id.
    A negative tally id means that the Variable object doesn't belong to a tally
    """
    def __init__(self, symbol, tally_id=0):        
        assert isinstance(symbol, str) and isinstance(tally_id, int)
        self.symbol = symbol
        self.tally_id = tally_id
        
    def __repr__(self): return '%s%d' % (self.symbol, self.tally_id) if self.tally_id!=0 else self.symbol
    
    def is_in(self, expr):
        if   expr is None:                   return False
        elif isinstance(expr, Constant):     return False
        elif isinstance(expr, Type):         return False
        elif isinstance(expr, Variable):     return self == expr
        elif isinstance(expr, Function):     return any(self.is_in(t) for t in expr)
        elif isinstance(expr, Clause):       return self.is_in(expr.head) or any(self.is_in(batom) for batom in expr)
        elif isinstance(expr, Literal):      return self.is_in(expr.atom)
        elif isinstance(expr, Goal):         return any(self.is_in(lit) for lit in expr)
        else: raise NotImplementedError(expr.__class__.__name__)
        
class Type(Term):
    def __init__(self, sign, name):
        self.sign = sign
        self.name = name
        
    def __repr__(self):
        return self.sign+str(self.name)     