from abc import ABC, abstractmethod
from aloe.clause import Constant, Variable, Operator

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
            self.headlessclauses = [clause for clause in clauses if not clause.head]
            clauses = [clause for clause in clauses if clause.head]
            operators = [clause.head for clause in clauses]
        self.allclauses = set()
        self.clausesbyoperator = dict()
        self.collec = dict()
        for op, clause in zip(operators, clauses):
            self.add(op, clause)
            
    def add(self, func, clause):
        fname = func.longname
        
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
            elif isinstance(term, Operator):
                if 'Funcs' not in term_dict:
                    term_dict['Funcs'] = TreeBasedClauseCollection([],[])                       
                term_dict['Funcs'].add(term,clause)
            
    def match(self, expr):
        name = expr.longname
        print(name, self.collec)
        if name not in self.collec:
            return set()
        sets = []
        for term, term_dict in zip(expr, self.collec[name]):
            print('Term',term)
            if   isinstance(term, Constant):
                if term.value in term_dict:
                    sets.append(term_dict[term.value] | term_dict['Vars'])
                else:
                    sets.append(term_dict['Vars'])
            elif isinstance(term, Variable):
                sets.append(self.clausesbyoperator[name])
            elif isinstance(term, Operator):
                sets.append(term_dict['Funcs'].match(term))
        print('Sets',sets)
        return set.intersection(*sets)
            
    def __repr__(self):
        return repr(self.collec)  