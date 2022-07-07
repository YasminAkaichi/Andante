from abc import ABC, abstractmethod
from aloe.logic_concepts import Constant, Variable, Function

class ClauseCollection(ABC):
    """ Collection of aloe.logic_concepts.Clause objects """
    @abstractmethod
    def add(self, clause):
        """ Adds a clause to the collection """
        pass
    
    @abstractmethod
    def remove(self, clause):
        """ Removes a clause from the collection """
        pass
    
    @abstractmethod
    def match(self, atom):
        """ Finds a clause from the collection whose head matches the input atom """
        pass

class TreeBasedClauseCollection(ClauseCollection):
    """ Collection where clauses are stored as a tree
    
    Attributes
    ----------
    allclauses : set of aloe.logic_concepts.Clause
        Set of all clauses represented by the tree
    clausesbyoperator : dict of sets of aloe.logic_concepts.Clause
        Given a function name, returns the set of all clauses whose head matches that function name
    collec : dict
        The tree collection of clauses
    """
    def __init__(self, clauses=None, operators=None):
        if clauses is None:
            clauses = []
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
                
    def remove(self, clause, func=None):
        if clause not in self.allclauses:
            return
        if func is None: func = clause.head
        fname = func.name
        
        self.allclauses.remove(clause)
        self.clausesbyoperator[fname].remove(clause)
        
        for term, term_dict in zip(func, self.collec[fname]):
            if isinstance(term, Constant):
                term_dict[term.value].remove(clause)
                if not term_dict[term.value]:
                    del term_dict[term.value]
            elif isinstance(term, Variable):
                term_dict['Vars'].remove(clause)                        
            elif isinstance(term, Function):
                term_dict['Funcs'].remove(clause, term)        
                
        if not self.clausesbyoperator[fname]:
            del self.clausesbyoperator[fname]
            del self.collec[fname]
                
            
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