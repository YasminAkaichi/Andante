"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.

Acknowlegment
-------------

This software has benefited from the support of Wallonia thanks to the funding
of the ARIAC project (https://trail.ac), a project part of the
DigitalWallonia4.ai initiative (https://www.digitalwallonia.be).

It was done by Simon Jacquet at the University of Namur (https://www.unamur.be)
in the period of October 1st 2021 to August 31st 2022 under the supervision of
Isabelle Linden, Jean-Marie Jacquet and Wim Vanhoof. 
"""

from abc import ABC, abstractmethod

from andante.options import Options
from andante.logic_concepts  import (
    Atom, 
    Clause, 
    Constant, 
    Variable, 
    Function,
)
from andante.collections import OrderedSet

from collections.abc import Iterable
from itertools import chain

class Knowledge(ABC):
    """ Collection of clauses """
    @property
    @abstractmethod
    def __iter__(self):
        """ Returns an iterator that goes through all clauses """
        pass

    @abstractmethod
    def match(self, atom):
        """ Return all clauses that match some atom """
        pass
    
    @abstractmethod
    def add(self, clause):
        """ Add some clause to the current knowledge """
        pass
    
    @abstractmethod
    def remove(self, clause):
        """ Remove some clause from the current knowledge """
        pass
    
    def copy(self):
        return self.__class__([c for c in self])

    def __repr__(self) -> str:
        name = 'Knowledge object (class: %s)\n' % self.__class__.__name__
        tab = ' '*3
        tab_repr = [tab+repr(c) for c in self]
        content = 'Clauses:\n' + '\n'.join(tab_repr)
        return name + content

class MultipleKnowledge(Knowledge):
    """ Knowledge composed of multiple sub-knowledges """
    def __init__(self, *knowledges, options=None):
        assert len(knowledges) >= 1
        self.options = options if options is not None else Options()
        self.knowledges = knowledges
        
    def __iter__(self):
        return iter(chain(*self.knowledges))
        
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
    
    # def __repr__(self):
    #     tab = ' '*3
    #     tab_repr = [tab+repr(k).replace('\n','\n'+tab) for k in self.knowledges]
    #     return 'MultipleKnowledge object\n'+'\n\n'.join(tab_repr)
    
    def copy(self):
        return MultipleKnowledge(*[k.copy() for k in self.knowledges], self.options)


class TreeShapedKnowledge(Knowledge):
    """ Knowledge stored as a tree of clauses
    
    Attributes
    ----------
    allclauses : set of andante.logic_concepts.Clause
        Set of all clauses represented by the tree
    clausesbyoperator : dict of sets of andante.logic_concepts.Clause
        Given a function name, returns the set of all clauses whose head matches that function name
    collec : dict
        The tree collection of clauses
    """
    def __init__(self, clauses=None, operators=None, options=None):
        self.options = options
        if clauses is None:
            clauses = []
        if operators is None:
            operators = [clause.head for clause in clauses]
        self.clauses = OrderedSet()
        self.clausesbyoperator = dict()
        self.collec = dict()
        for op, clause in zip(operators, clauses):
            self.add(clause, op)

    def __iter__(self):
        return iter(self.clauses)
            
    def add(self, clause, func=None):
        # In case input is not a clause but an iterable containing clauses
        if not isinstance(clause, Clause):
            if not isinstance(clause, Iterable):
                raise KeyError('Expected andante.logic_concepts.Clause or Iterable object, found : %s' % clause.__class__.__name__)
            for x in clause:
                self.add(x)
            return

        if func is None: func = clause.head
        fname = func.name
        
        self.clauses.add(clause)
        
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
                    term_dict['Funcs'] = TreeShapedKnowledge([],[])                       
                term_dict['Funcs'].add(clause, term)
                
    def remove(self, clause, func=None):
        # In case input is not a clause but an iterable containing clauses
        if not isinstance(clause, Clause):
            if not isinstance(clause, Iterable):
                raise KeyError('Expected andante.logic_concepts.Clause or Iterable object, found : %s' % clause.__class__.__name__)
            for x in clause:
                self.remove(x)
            return

        if clause not in self.clauses:
            return
        if func is None: func = clause.head
        fname = func.name
        
        self.clauses.remove(clause)
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
