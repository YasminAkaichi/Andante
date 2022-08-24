import math
from abc import ABC, abstractmethod
from andante.logic_concepts import (
    Atom, 
    LogicConcept,
    Variable,
    Constant,
)

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


