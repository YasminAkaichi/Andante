from abc import ABC, abstractmethod
from aloe.clause import Constant, Variable, Function

class ClauseCollection(ABC):
    @abstractmethod
    def add(self, func, clause):
        pass
    
    @abstractmethod
    def match(self, atom):
        pass

class TreeBasedClauseCollection(ClauseCollection):
    def __init__(self, clauses, operators=None):
        if operators is None:
            operators = [clause.head for clause in clauses]
        self.allclauses = set()
        self.clausesbyoperator = dict()
        self.collec = dict()
        for op, clause in zip(operators, clauses):
            self.add(clause, op)
            
    def add(self, clause, func=None):
        if func is None: func = clause.head
        fname = func.name
        
        self.allclauses.add(clause)
        
        if fname not in self.clausesbyoperator:
            self.clausesbyoperator[fname] = set()
        self.clausesbyoperator[fname].add(clause)
            
        if fname not in self.collec:
            self.collec[fname] = [{'Vars':set()} for _ in range(func.arity)]
        for term, term_dict in zip(func, self.collec[fname]):
            if isinstance(term, Constant):
                if not term.value in term_dict:
                    term_dict[term.value] = set()
                term_dict[term.value].add(clause)    
            elif isinstance(term, Variable):
                term_dict['Vars'].add(clause)                        
            elif isinstance(term, Function):
                if 'Funcs' not in term_dict:
                    term_dict['Funcs'] = TreeBasedClauseCollection([],[])                       
                term_dict['Funcs'].add(clause, term)
            
    def match(self, expr):
        name = expr.name
        if name not in self.collec:
            return set()
        sets = []
        for term, term_dict in zip(expr, self.collec[name]):
            if   isinstance(term, Constant):
                if term.value in term_dict:
                    sets.append(term_dict[term.value] | term_dict['Vars'])
                else:
                    sets.append(term_dict['Vars'])
            elif isinstance(term, Variable):
                sets.append(self.clausesbyoperator[name])
            elif isinstance(term, Function):
                sets.append(term_dict['Funcs'].match(term))
        return set.intersection(*sets)
            
    def __repr__(self):
        return repr(self.collec)  