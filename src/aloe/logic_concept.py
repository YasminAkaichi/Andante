from abc import ABC, abstractmethod

class LogicConcept(ABC):
    """ Class representing all logic concepts. """
    @abstractmethod
    def apply(self, fun):
        """ Applies the function :meth:`fun` to all sub-LogicConcepts if any.
        
        sub-LogicConcepts are any LogicConcept object present as attributes of another LogicConcept
        Ex: 
            - Clauses have Atoms as sub-LogicConcepts
            - Predicates have Terms as sub-LogicConcepts
            - Variables have no sub-LogicConcepts
        
        Parameters:
            - fun (function): the function to apply.
            
        Returns:
            - ``None`` or a new :class:`LogicConcept` on which :param:`fun` has been applied.
        """
        pass
    
    
class Clause(LogicConcept):
    """ Represents a horn clause in first order logic. """
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
    """ Represents a goal as a list of atoms or negations. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert all((isinstance(l, (Atom, Negation)) for l in self))        

    def __repr__(self): return ','.join(repr(expr) for expr in self)        

    def apply(self, fun): 
        try: return Goal(expr.apply(fun) for expr in self)
        except AssertionError:
            return None        
        
class Negation(LogicConcept):
    """ Represents the negation of a goal """
    def __init__(self, goal):
        assert isinstance(goal, Goal)
        self.goal = goal
        
    def __repr__(self): return 'not(%s)' % repr(self.goal)
        
    def apply(self, fun): 
        try: return Negation(self.goal.apply(fun))
        except AssertionError:
            return None        
    
class Function(LogicConcept, ABC):
    """ 
    Represents a function as the general form of a predicate and a CompoundTerm.
    
    Attributes:
        - functor (str): name of the function.
        - arguments (:class:`list` of :class:`Term`): arguments of the function
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
    
    def apply(self, fun):
        args = [arg.apply(fun) for arg in self.arguments]
        try:    return self.__class__(self.functor, args)
        except: return None
    
class Atom(LogicConcept, ABC):
    """ Represents an atom in the first order logic framework """
    def __hash__(self):      return hash(str(self))
    def __eq__(self, other): return str(self) == str(other)    
    
class Term(LogicConcept, ABC):
    """ Represents a term in the first order logic framework """
    def __hash__(self):      return hash(str(self))
    def __eq__(self, other): return str(self) == str(other)
    
    @abstractmethod
    def unify(self, other, subst): pass

class Predicate(Atom, Function): 
    """ 
    Represents a predicate in first order logic.
    """
    pass

class CompoundTerm(Term, Function):
    """ 
    This class represents compound terms as defined in the prolog framework.
    """
    def unify(self, other, subst):
        if   isinstance(other, Variable):
            other.unify(self, subst)
        elif (
            (isinstance(self, other.__class__) or isinstance(other, self.__class__)) and \
            self.functor == other.functor
        ):
            for self_arg, other_arg in zip(self.arguments, other.arguments):
                self_arg.unify(other_arg, subst)
        else: raise UnificationException(self, other)
    
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
        else: raise UnificationException(self, other)
            
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
        output = False
        def fun(element):
            if isinstance(element, Variable) and element == expr:
                output = True
        expr.apply(fun)
        return output
            
    def apply(self, fun): return fun(self)
    
    def evaluate(self, subst): 
        if self in subst:
            return subst[self]
        else:
            raise Exception('Variable is not instantiated')

    def unify(self, other, subst):
        subst[self] = other
            
class Type(Term):
    """ 
    In progol, a term for a mode can be a type '+person' composed of a sign ('+', '-' or '#') and a name ('person')
    """
    def __init__(self, sign, name):
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
        else: raise UnificationException(self, other)

            
    
#######################################################
# Classes related to explicit mathematical expressions
#######################################################    

import math

class Comparison(Atom, ABC):        
    def __init__(self, arg1, arg2, symbol):
        assert arg1 is not None and arg2 is not None
        self.arg1 = arg1
        self.arg2 = arg2
        self.symbol = symbol
        
    @abstractmethod
    def evaluate(self, subst):
        pass
        
    def __repr__(self): return '%s %s %s' % (repr(self.arg1), self.symbol, repr(self.arg2))
    
    def apply(self, fun):
        try:    return self.__class__(self.arg1.apply(fun), self.arg2.apply(fun), self.symbol)
        except: return None


arithmetic_symbol_table = {
    '=:=' : lambda x, y: x==y,
    '=\=' : lambda x, y: x!=y,
    '<'   : lambda x, y: x<y,
    '<='  : lambda x, y: x<=y,
    '>'   : lambda x, y: x>y,
    '>='  : lambda x, y: x>=y, 
}    
class ArithmeticComparison(Comparison):        
    def evaluate(self, subst):
        expr1 = self.arg1.evaluate(subst) 
        expr2 = self.arg2.evaluate(subst)
        return arithmetic_symbol_table[self.symbol](expr1, expr2)

    
unification_symbol_table = {
    '=='  : lambda x, y: x==y,
    '\==' : lambda x, y: x!=y,
    '@<'  : lambda x, y: x<y,
    '@<=' : lambda x, y: x<=y,
    '@>'  : lambda x, y: x>y,
    '@>=' : lambda x, y: x>=y,
}

class UnificationComparison(Comparison):
    def evaluate(self, subst):
        if self.symbol == '=':
            try: 
                subst.unify(self.arg1, self.arg2)
                return True
            except:
                return False
        elif self.symbol == '\=':
            try:
                subst2 = subst.copy()
                subst2.unify(self.arg1, self.arg2)
                return False
            except:
                return True
        else:
            return unification_symbol_table[self.symbol](str(self.arg1), str(self.arg2))
    
    
class ArithmeticExpression(LogicConcept, ABC):
    @abstractmethod
    def evaluate(self, subst):
        pass
    
    @abstractmethod
    def apply(self, fun):
        pass
    
class ParenthesisArithmeticExpression(ArithmeticExpression):
    def __init__(self, expr):
        assert expr is not None
        self.expr = expr
        
    def evaluate(self, subst): return self.expr.evaluate(subst)
    
    def apply(self, fun):
        try:    return self.__class__(self.expr.apply(fun))
        except: return None
        
    def __repr__(self): return '(%s)' % repr(self.expr)
    
basic_arithmetic_symbol_table = {
    '+' : lambda x, y: x+y,
    '-' : lambda x, y: x-y,
    '/' : lambda x, y: x/y,
    '*' : lambda x, y: x*y,
    '**': lambda x, y: x**y,
    'mod':lambda x, y: x%y,
    '//': lambda x, y: x//y,
}
symbol_prioritiy = {
    '+' : 1,
    '-' : 1,
    '/' : 2,
    '*' : 2,
    '**': 3,
    'mod':2,
    '//': 2,
}
class BasicArithmeticExpression(ArithmeticExpression):    
    def __init__(self, expr1, expr2, symbol):
        assert expr1 is not None and expr2 is not None
        if   isinstance(expr1, BasicArithmeticExpression) and symbol_prioritiy[expr1.symbol]<symbol_prioritiy[symbol]:
            self.expr1  = expr1.expr1
            self.expr2  = BasicArithmeticExpression(expr1.expr2, expr2, symbol)
            self.symbol = expr1.symbol
        elif isinstance(expr2, BasicArithmeticExpression) and symbol_prioritiy[expr2.symbol]<symbol_prioritiy[symbol]:
            self.expr1  = BasicArithmeticExpression(expr1, expr2.expr1, symbol)
            self.expr2  = expr2.expr2
            self.symbol = expr2.symbol
        else:
            self.expr1  = expr1
            self.expr2  = expr2
            self.symbol = symbol
        
    def evaluate(self, subst):
        return basic_arithmetic_symbol_table[self.symbol](self.expr1.evaluate(subst), self.expr2.evaluate(subst))
    
    def apply(self, fun):
        try: 
            return self.__class__(self.expr1.apply(fun), self.expr2.apply(fun), self.symbol)
        except: return None
        
    def __repr__(self): return '%s%s%s' % (repr(self.expr1), self.symbol, repr(self.expr2))

class TrigoExpression(ArithmeticExpression):
    def __init__(self, expr, symbol):
        assert expr is not None
        self.expr = expr
        self.symbol = symbol
        self.symbol_function = getattr(math, symbol)
        
    def evaluate(self, subst):
        return self.symbol_function(self.expr.evaluate(subst))
    
    def apply(self, fun):
        try: return self.__class__(self.expr.apply(fun), self.symbol)
        except: return None
        
    def __repr__(self): return '%s(%s)' % (self.symbol, repr(self.expr))

class Is(Atom):
    def __init__(self, arg1, arg2):
        assert isinstance(arg1, (Variable, Constant)) and isinstance(arg2, (Variable, Constant, ArithmeticExpression))
        self.arg1 = arg1
        self.arg2 = arg2
    
    def apply(self, fun): 
        try:    return self.__class__(self.arg1.apply(fun), self.arg2.apply(fun))
        except: return None
        
    def evaluate(self, subst):
        if isinstance(self.arg1, Constant):
            return self.arg1.value == self.arg2.evaluate(subst)
        else:
            try:
                if isinstance(self.arg2, Variable):
                    subst[self.arg1] = self.arg2
                else:
                    subst[self.arg1] = self.arg2.evaluate(subst)
                return True
            except: return False
        
    def __repr__(self): return '%s is %s' % (repr(self.arg1), repr(self.arg2))


    
#######################################################
# Utility functions related to classes defined above
#######################################################


class UnificationException(Exception):
    def __init__(self, term1, term2):
        message = 'Cannot unify terms <%s> and <%s>' % (str(term1), str(term2))
        super().__init__(message)


class List(Term):
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
                    raise UnificationException(self.elements2, new_other)
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



    



