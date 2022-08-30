"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.
"""

import andante.solver
import andante.learner
from andante.logic_concepts    import Goal, Clause, Negation, Variable, extract_variables
from andante.options   import Options
from andante.mode      import ModeCollection, Modeh
from andante.knowledge import Knowledge, TreeShapedKnowledge, MultipleKnowledge
from andante.substitution import Substitution
from andante.utils import generate_variable_names
import itertools
import pandas

class AndanteProgram:
    def __init__(self, options=None, knowledge=None, modes=None, examples=None):
        """ Class representing a Andante program

        Attributes
        ----------
        options : andante.options.Options
            Options for the object
        knowledge : andante.knowledge.Knowledge 
            Collection of clauses, background knowledge
        examples : dict 
            Dictionnary of positive and negative examples 
        solver : andante.solver.Solver 
            Deduction engine, handles all queries
        modes : andante.modes.ModeCollection 
            Collection of modes and determinations
        learner : andante.learner.Learner 
            Induction engine, handles learning
        """
        self.options   = options   if options   else Options()
        self.knowledge = knowledge if knowledge else TreeShapedKnowledge(options=self.options)
        self.solver    = getattr(andante.solver, self.options.solver)(options=self.options)
        self.modes     = modes     if modes     else ModeCollection(options=self.options)
        self.examples  = examples  if examples  else {'pos':[], 'neg':[]}
        self.learner   = getattr(andante.learner, self.options.learner)(options=self.options)
        
    @property
    def parser(self):
        """ Returns a andante.parser.Parser object """
        if not hasattr(self, '_parser'):
            import andante.parser
            self._parser = andante.parser.Parser()
        return self._parser
        
    @staticmethod
    def build_from(andantefile): 
        """ Returns the corresponding AndanteProgram """
        import andante.parser
        return andante.parser.Parser().parse(andantefile, 'andantefile')    
    
    @staticmethod
    def build_from_background(text):
        """ Returns the corresponding AndanteProgram """
        return AndanteProgram.build_from(':-begin_bg.\n%s\n:-end_bg.' % (text))
        
    def __repr__(self):
        """ Get string representation of the object """
        B = repr(self.knowledge)
        E = 'Positive:\n%s\nNegative:\n%s' % ('\n'.join(repr(e) for e in self.examples['pos']),
                                              '\n'.join(repr(e) for e in self.examples['neg']))
        M = repr(self.modes)
        o = repr(self.options)
        return 'Background:\n%s\n\nExamples:\n%s\n\nModes:\n%s\n\noptions:\n%s' % (B,E,M,o)
        
    def query(self, q, **temp_options):
        """ Launch a query to the andante solver. 

        Parameters
        ----------
        q : str or andante.logic_concepts.Goal
            The query to be evaluated

        Returns
        -------
        bool
            Whether there exists a substitution for the query
        pandas.DataFrame
            Tabular aggregating all substitutions possible for the query.
            Columns correspond to varibles.
            Rows correspond to the various possible substitutions.
        """
        assert isinstance(q, (str, Goal))
        if isinstance(q, str):
            q = self.parser.parse(q, 'query')
        sigmas = list(self.solver.query(q, self.knowledge, **temp_options))
        
        if not sigmas:
            return False, []
        else:
            data = dict()
            all_var = set()
            for i, sigma in enumerate(sigmas):
                data[i] = list()
                for var, value in sigma.subst.items():
                    data[i].append(value)
                    all_var.add(var)
                    
            pandas_out = pandas.DataFrame(data=data, index=all_var)
            return True, pandas_out
    
    def verify(self, c, **temp_options):
        """ Verify whether some clause is true, given the current background knowledge """
        assert isinstance(c, (str, Clause))
        if isinstance(c, str):
            c = self.parser.parse(c)
        goal = Goal([Negation(Goal(c.body + [Negation(Goal([c.head]))]))])
        return self.query(goal, **temp_options)
    
    def set(self, field, value):
        """ Set an option to a new value """
        self.options[field] = value
        
    def induce(self, **temp_options):
        """ Launches the learning process for new clauses """
        return self.learner.induce(self.examples, self.modes, self.knowledge, self.solver, **temp_options)

    def generate_examples(self, text, update_examples=True):
        """
        
        """
        if isinstance(text, str):
            new_knowledge, lmodes = self.parser.parse(text, 'generator')
            for mode in lmodes:
                self.modes.add(mode)
        
        examples = {'pos':[], 'neg':[]}
        knowledge = MultipleKnowledge(self.knowledge, new_knowledge)
        
        for modeh in [x for x in lmodes if isinstance(x, Modeh)]:
            matom = modeh.atom
            generator = generate_variable_names()
            template = matom.__class__(matom.symbol, [Variable(next(generator)) for _ in matom.arguments])
            mapping = {var:t.name for var, t in zip(template.arguments, matom.arguments)}
            #mapping = {var:mapping[repr(var)] for var in extract_variables(clause.head)}

            T = dict()
            for var in mapping:
                T[var] = list()
                atom = self.parser.parse(mapping[var]+'(X)', 'predicate')
                for matched_clause in self.knowledge.match(atom):
                    # The clause must be bodyless
                    if len(matched_clause.body)>0:
                        continue
                    skolem, = matched_clause.head.arguments
                    T[var].append(skolem)

            S = [[(var, skolem) for skolem in T[var]] for var in T]


            for s in itertools.product(*S):
                query = Substitution().rename_variables(template, subst=dict(s))
                if self.solver.succeeds_on(query, knowledge):
                    examples['pos'].append(Clause(query,[]))
                else:
                    examples['neg'].append(Clause(query,[]))
                
        if update_examples:
            self.examples['pos'].extend(examples['pos'])
            self.examples['neg'].extend(examples['neg'])
            
        return examples
    
    
    
    def generate_examples_from_clause(self, clause, mapping, update_examples=True):
        """
        clause: the clause that generates examples
        mapping: dict that maps unbounded variables to 
        """
        if isinstance(clause, str):
            clause = self.parser.parse(clause, 'hornclause')
        
        mapping = {var:mapping[repr(var)] for var in extract_variables(clause.head)}
        
        T = dict()
        for var in mapping:
            T[var] = list()
            atom = self.parser.parse(mapping[var]+'(X)', 'predicate')
            for matched_clause in self.knowledge.match(atom):
                # The clause must be bodyless
                if len(matched_clause.body)>0:
                    continue
                skolem, = matched_clause.head.arguments
                T[var].append(skolem)
                
        S = [[(var, skolem) for skolem in T[var]] for var in T]
        
        examples = {'pos':[], 'neg':[]}
        
        for s in itertools.product(*S):
            c = Substitution().rename_variables(clause, subst=dict(s))
            goal = Goal(c.body)
            success, _ = self.query(goal)
            if success:
                examples['pos'].append(Clause(c.head,[]))
            else:
                examples['neg'].append(Clause(c.head,[]))
                
        print(len(examples['pos']),len(examples['neg']))
        if update_examples:
            self.examples['pos'].extend(examples['pos'])
            self.examples['neg'].extend(examples['neg'])
            
        return examples
