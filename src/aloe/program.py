import aloe.solver
import aloe.learner
from aloe.logic_concept    import Goal, Clause, Negation, Variable, extract_variables
from aloe.options   import Options
from aloe.mode      import ModeCollection, Modeh
from aloe.knowledge import Knowledge, LogicProgram, MultipleKnowledge
from aloe.substitution import Substitution
from aloe.utils import generate_variable_names
import itertools
import pandas

class AloeProgram:
    def __init__(self, options=None, knowledge=None, modes=None, examples=None):
        """
        Class representing a Aloe program
        Attributes :
            - options:   see aloe.options
            - knowledge: gathers all clauses (aloe.knowledge.Knowledge object)
            - examples:  dictionnary of positive and negative examples 
            - solver:    handles all queries (aloe.solver.Solver object)
            - modes:     assembles modes and determinations (aloe.modes.ModeCollection object)
            - learner:   handles inductive learning (aloe.learner.Learner object) 
            -B: background knowledge
            -E: examples
            -M: modes
            -options: options
        """
        self.options   = options   if options   else Options()
        self.knowledge = knowledge if knowledge else LogicProgram(options=self.options)
        self.solver    = getattr(aloe.solver, self.options.solver)(options=self.options)
        self.modes     = modes     if modes     else ModeCollection(options=self.options)
        self.examples  = examples  if examples  else {'pos':[], 'neg':[]}
        self.learner   = getattr(aloe.learner, self.options.learner)(options=self.options)
        
    @property
    def parser(self):
        if not hasattr(self, '_parser'):
            import aloe.parser
            self._parser = aloe.parser.AloeParser()
        return self._parser
        
    @staticmethod
    def build_from(aloefile): 
        import aloe.parser
        return aloe.parser.AloeParser().parse(aloefile, 'aloefile')    
    
    @staticmethod
    def build_from_background(text):
        return AloeProgram.build_from(':-begin_bg.\n%s\n:-end_bg.' % (text))
        
    def __repr__(self):
        B = repr(self.knowledge)
        E = 'Positive:\n%s\nNegative:\n%s' % ('\n'.join(repr(e) for e in self.examples['pos']),
                                              '\n'.join(repr(e) for e in self.examples['neg']))
        M = repr(self.modes)
        o = repr(self.options)
        return 'Background:\n%s\n\nExamples:\n%s\n\nModes:\n%s\n\noptions:\n%s' % (B,E,M,o)
        
    def query(self, q, **temp_options):
        """
        Launch a query to the aloe solver. 
        The query 'q' can be:
        - a string: the query will then first be parsed and then evaluated
        - a goal
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
        """
        Verify whether clause is true 
        """
        assert isinstance(c, (str, Clause))
        if isinstance(c, str):
            c = self.parser.parse(c)
        goal = Goal([Negation(Goal(c.body + [Negation(Goal([c.head]))]))])
        return self.query(goal, **temp_options)
    
    def set(self, field, value): self.options[field] = value
        
    def induce(self, **temp_options):
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
            template = matom.__class__(matom.functor, [Variable(next(generator)) for _ in matom.arguments])
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
