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
import pickle
import dill as pickle  

class AndanteProgram:
    def __init__(self, options=None, knowledge=None, modes=None, examples=None,results=None,parameters=None):
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
        self.results = results
        self.parameters= parameters

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
                    
            pandas_out = pandas.DataFrame(data=data, index=list(all_var))
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
    
    def save(self, filename):
        """Saves the current AndanteProgram instance to a file using pickle."""
        solver_backup = self.solver  # Backup the solver
        self.solver = None
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        self.solver = solver_backup  # Restore the solver
        print(f"AndanteProgram saved to {filename}")

    @staticmethod
    def load(filename):
        """Loads an AndanteProgram instance from a file."""
        with open(filename, 'rb') as f:
            instance = pickle.load(f)
        instance.solver = getattr(andante.solver, instance.options.solver)(options=instance.options)
        return pickle.load(f)
        
        
    def add_background_knowledge(self,bk):
        """Add a Bk to an AndanteProgram from text"""
        self.knowledge.add(bk)


    def infer_and_explain(self, new_data):

        """Infer and explain recommendations for a new user based on the induced rules.
        
        Parameters
        ----------
        new_data : dict
            Dictionary containing the new user's data (features).
        
        Returns
        -------
        dict
            A dictionary containing the recommendation and the explanation of why it was made.
        """
        recommendations = []
        explanations = []

        # Iterate through the induced rules in `results`
        for rule in self.results:
            # Match the new user's data against the conditions in the rule's body.
            match = True
            explanation = []
            for condition in rule.body:
                # Here we would match each condition in the rule body with the user's data
                # Example: if the rule has a condition on a specific feature, compare it with the new_user_data
                feature = condition.symbol
                expected_value = condition.arguments[0]

                if new_data.get(feature) == expected_value:
                    explanation.append(f"{feature} = {expected_value}")
                else:
                    match = False
                    break
            
            if match:
                # If all conditions match, this rule applies, so recommend the rule's head and explain why
                recommendations.append(rule.head)
                explanations.append(f"Recommendation based on: {' and '.join(explanation)}")

        return {
            'recommendations': recommendations,
            'explanations': explanations
        }
    

    def query_with_explanation(self, q, new_facts=None, induce_new_rules=False, **temp_options):
        """Launch a query to the Andante solver, integrating new data and returning explanations.
        Parameters
        ----------
        q : str or andante.logic_concepts.Goal
            The query to be evaluated.
        new_facts : str or list of str, optional
            New facts to be added to the knowledge base before the query.
        induce_new_rules : bool, optional
            If True, induces new rules based on updated facts and examples.
        **temp_options : Additional options for the solver.

        Returns
        -------
        bool
            Whether there exists a substitution for the query.
        pandas.DataFrame
            Tabular aggregating all substitutions possible for the query.
        str
            An explanation of which rules or facts led to the prediction.
        """
        # Step 1: Add new facts to the knowledge base if provided
        if new_facts:
            if isinstance(new_facts, str):
                new_facts = [new_facts]
            for fact in new_facts:
                self.add_background_knowledge_from_text(fact) 

        # Step 2: Induce new rules if requested
        if induce_new_rules:
            self.results = self.induce()

        # Step 3: Ensure induced rules from self.results are added to the knowledge base
        for rule in self.results:
            self.knowledge.add(rule)

        # Step 4: Parse the query
        assert isinstance(q, (str, Goal))
        if isinstance(q, str):
            q = self.parser.parse(q, 'query')

        # Step 5: Execute the query using the Andante solver
        sigmas = list(self.solver.query(q, self.knowledge, **temp_options))

        # Step 6: If the query fails, return no result
        if not sigmas:
            return False, [], "No matching rules found."

        # Step 7: If the query succeeds, gather possible substitutions and build an explanation
        data = dict()
        all_var = set()
        explanations = []

        for i, sigma in enumerate(sigmas):
            data[i] = list()
            for var, value in sigma.subst.items():
                data[i].append(value)
                all_var.add(var)
            # Step 8: Generate explanations based on matching rules
            # Check which rules matched for this substitution
            matching_rules = self._find_matching_rules(q, sigma)
            explanations.append(f"Matched rule(s): {', '.join(matching_rules)}")

        # Convert the results into a pandas DataFrame
        pandas_out = pandas.DataFrame(data=data, index=list(all_var))

        # Step 9: Return the result with explanations
        return True, pandas_out, '\n'.join(explanations)

    def _find_matching_rules(self, query, sigma):
        """Helper method to find which rules matched for a given query and substitution.
        
        Parameters
        ----------
        query : Goal
            The query being evaluated.
        sigma : Substitution
            The substitution that was applied during the query.
        
        Returns
        -------
        list
            A list of rule descriptions that matched the query.
        """
        matching_rules = []
        # Iterate through learned rules in self.results and check if they apply
        for rule in self.results:
            if self.solver.succeeds_on(query, self.knowledge):
                matching_rules.append(str(rule))
        return matching_rules
    
    def add_background_knowledge_from_text(self, bk_text):
        """Add new background knowledge to the AndanteProgram.
    
        Parameters
        ----------
        bk_text : str
        Background knowledge in text format to be added to the knowledge base.
        """
        # Debug: Print the background knowledge text before parsing
        print("Background knowledge being added:\n", bk_text)
    
        # Parse and add the new background knowledge
        try:
            #new_knowledge = self.parser.parse(bk_text, 'knowledge')
            new_knowledge = self.parser.parse(bk_text, rule='background')
            self.knowledge.add(new_knowledge)
            print("Background knowledge added successfully.")
        except Exception as e:
            print(f"Error parsing background knowledge: {e}")
