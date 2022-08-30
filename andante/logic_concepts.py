"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.
"""

from abc import ABC, abstractmethod
from typing import Literal

# TODO: Remove all unify functions as they are redundant with the unify function
# in andante.substitution.Substitution
class LogicConcept(ABC):
    """ Any logic concept of first order logic """
    @abstractmethod
    def apply(self, fun):
        """ Transforms all underlying logic concepts of the object, or if none, the object itself
        
        Examples
        --------
        Clauses have their atoms transformed
        Predicates have their terms transformed
        Variables are transformed
        
        Parameters
        ----------
        fun : function
            The function that transforms logic concepts
            
        Returns
        -------
        andante.logic_concepts.LogicConcept
            The transformed logic concept
        """
        pass
    
    
class Clause(LogicConcept):
    """ Horn clause in first order logic """
    def __init__(self, head, body):
        assert isinstance(head, Atom) or head is None
        assert isinstance(body, list) and all((isinstance(batom, Atom) for batom in body))
        self.head = head
        self.body = body
                
    def __repr__(self):
        head_repr = repr(self.head)
        body_repr = ', '.join([repr(term) for term in self.body])
        if not self.body: return '%s.'     % (head_repr)
        elif self.head:   return '%s :- %s.' % (head_repr, body_repr)
        else:             return ':- %s.'   % (body_repr)
        
    def __hash__(self):      return hash(str(self))
    def __eq__(self, other): return str(self)==str(other)
    
    def apply(self, fun):
        h = self.head.apply(fun)
        b = [b.apply(fun) for b in self.body]
        try: return Clause(h, b)
        except AssertionError:
            return None
    
class Goal(list, LogicConcept): 
    """ Goal in first order logic """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert all((isinstance(l, (Atom, Negation)) for l in self))        

    def __repr__(self): return ', '.join(repr(expr) for expr in self)        

    def apply(self, fun): 
        try: return Goal(expr.apply(fun) for expr in self)
        except AssertionError:
            return None        
        
class Negation(LogicConcept):
    """ Negation of a goal in first order logic """
    def __init__(self, goal: Goal):
        assert isinstance(goal, Goal)
        self.goal = goal
        
    def __repr__(self): return 'not(%s)' % repr(self.goal)
        
    def apply(self, fun): 
        try: return Negation(self.goal.apply(fun))
        except AssertionError:
            return None        
    
class Function(LogicConcept, ABC):
    """ Function as the general form of a Predicate and a CompoundTerm
    
    Attributes
    ----------
    symbol : str
        the symbol, i.e. the name of the function
    arguments : list of andante.logic_concepts.Term
        the inputs of the function
    """
    def __init__(self, symbol: str, arguments: list):
        assert isinstance(symbol, str)
        assert isinstance(arguments, (list,tuple)) and all((isinstance(arg, Term) for arg in arguments))
        self.symbol   = symbol
        self.arguments = arguments
        
    @property
    def name(self): return '%s/%d' % (self.symbol,self.arity)
    @property
    def arity(self): return len(self.arguments)
    
    def __iter__(self): return iter(self.arguments)    
    def __repr__(self): return '%s(%s)' % (self.symbol, ', '.join([repr(arg) for arg in self.arguments]))
    
    def apply(self, fun):
        args = [arg.apply(fun) for arg in self.arguments]
        try:    return self.__class__(self.symbol, args)
        except: return None
    
class Atom(LogicConcept, ABC):
    """ Atom in the first order logic framework """
    def __hash__(self):      return hash(str(self))
    def __eq__(self, other): return str(self) == str(other)    
    
class Term(LogicConcept, ABC):
    """ Term in the first order logic framework """
    def __hash__(self):      return hash(str(self))
    def __eq__(self, other): return str(self) == str(other)
    
    @abstractmethod
    def unify(self, other, subst): 
        """ Unify two terms
        
        Updates the andante.substitution.Substitution subst to take into account the unification of andante.logic_concepts.Term self and other
        
        Parameters
        ----------
        other : andante.logic_concepts.Term
            The term to unify with
        subst : andante.substitution.Substitution
            The current substitution
        """
        pass

class Predicate(Atom, Function): 
    """ Predicate in first order logic """
    pass

class CompoundTerm(Term, Function):
    """ Compound terms as defined in the prolog framework """
    def unify(self, other, subst):
        if   isinstance(other, Variable):
            other.unify(self, subst)
        elif (
            (isinstance(self, other.__class__) or isinstance(other, self.__class__)) and \
            self.symbol == other.symbol
        ):
            for self_arg, other_arg in zip(self.arguments, other.arguments):
                self_arg.unify(other_arg, subst)
        else: raise UnificationError(self, other)
    
class Constant(Term):
    """ Constant in first order logic
    
    Attributes
    ----------
    value : int or float or string
        Data held by the constant
    """
    def __init__(self, value):
        assert isinstance(value, (int, float, str))
        if isinstance(value, str) and value[0].isupper():
            message = 'String values of andante.logic_concepts.Constant must begin by a lowercase, got: %s' % value
            raise TypeError(message)
        self.value = value
        
    def __repr__(self): return str(self.value)
    
    def to_variable_name(self): # TODO change to to_variable_symbol
        """ Returns a valid unique variable symbol """
        if isinstance(self.value, str): return self.value.capitalize()
        else:                           return 'V' + str(self.value).replace('.','_')
        
    def apply(self, fun): return fun(self)
    
    def evaluate(self, subst): return self.value
    
    def unify(self, other, subst):
        if   isinstance(other, Variable):
            other.unify(self, subst)
        elif (
            (isinstance(self, other.__class__) or isinstance(other, self.__class__)) and \
            self == other
        ):
            return
        else: raise UnificationError(self, other)
            
class Variable(Term):
    """ Variable in the first order logic framework
    
    Attributes
    ----------
    symbol : string
        The symbol or name of the variable
    tally_id : int
        A number to differentiate different andante.logic_concepts.Variable objects with the same symbol
    """
    def __init__(self, symbol, tally_id=0):        
        assert isinstance(symbol, str) and isinstance(tally_id, int)
        self.symbol = symbol
        self.tally_id = tally_id
        
    def __repr__(self): return '%s%d' % (self.symbol, self.tally_id) if self.tally_id!=0 else self.symbol
    
    def is_in(self, expr):
        output = False
        def fun(element):
            nonlocal output
            if isinstance(element, Variable) and element == self:
                output = True
        expr.apply(fun)
        return output
            
    def apply(self, fun): return fun(self)
    
    def evaluate(self, subst): 
        if self in subst:
            return subst[self]
        else:
            raise KeyError('Variable (%s) is not instantiated' % str(self))

    def unify(self, other, subst):
        subst[self] = other
            
class Type(Term):
    """ Type as defined in the progol framework
    
    Examples
    --------
    +person
    #animal
    
    Attributes
    ----------
    sign : '+' or '-' or '#'
        '+' refers to input arguments, '-' refers to output arguments and '#' refers to constant
    name : str
    """
    def __init__(self, sign: Literal['+','-','#'], name: str):
        if sign not in ['+','-','#'] or not isinstance(name, str):
            raise(ValueError("sign should be '+', '-' or '#', got "+str(sign)))
        self.sign = sign
        self.name = name
        
    def __repr__(self):
        return self.sign+str(self.name)     
    
    def apply(self, fun): return fun(self)
    
    def unify(self, other, subst):
        if   isinstance(other, Variable):
            other.unify(self, subst)
        elif (
            (isinstance(self, other.__class__) or isinstance(other, self.__class__)) and \
            self == other
        ):
            return
        else: raise UnificationError(self, other)

class UnificationError(Exception):
    def __init__(self, term1, term2):
        message = 'Cannot unify terms <%s> and <%s>' % (str(term1), str(term2))
        super().__init__(message)


class List(Term):
    """ List in the prolog framework
    
    
    """
    " [a, b, c | B] "
    def __init__(self, e1, e2=None):
        self.elements1 = e1
        self.elements2 = e2
    
    def apply(self, fun):
        try:    
            e1 = [e.apply(fun) for e in self.elements1]
            e2 = self.elements2.apply(fun) if self.elements2 is not None else None
            return self.__class__(e1, e2)
        except: return None

    def __repr__(self): 
        s1 = ', '.join(repr(e) for e in self.elements1)
        if self.elements2 is None:
            return '[%s]' % (s1)
        else:
            s2 = repr(self.elements2)
            return '[%s | %s]' % (s1, s2)
        
    def unify(self, other, subst):
        if   isinstance(other, Variable):
            other.unify(self, subst)
        elif (
            isinstance(self, other.__class__) or isinstance(other, self.__class__)
        ):
            if len(self.elements1) > len(other.elements1):
                other.unify(self, subst)
                return
            for i in range(len(self.elements1)):
                self.elements1[i].unify(other.elements1[i], subst)
            
            if len(self.elements1) < len(other.elements1):
                new_other = List(other.elements1[len(self.elements1):], other.elements2)
            else:
                new_other = other.elements2
                
            if self.elements2 is None:
                if new_other is None:
                    return
                else:
                    raise UnificationError(self.elements2, new_other)
            else:
                self.elements2.unify(new_other, subst)
        

    
#######################################################
# Utility functions related to classes defined above
#######################################################

def extract_variables(expr):
    """ Returns as a set all Variables present in expr """
    variables = set()
    fun = lambda expr: variables.add(expr) if isinstance(expr, Variable) else None
    if isinstance(expr, (list, set)):
        for x in expr:
            variables.update(extract_variables(x))
    else:
        expr.apply(fun)
    return variables
