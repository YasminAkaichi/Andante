"""
All learners that build new knowledge

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

import re
import itertools
from abc import ABC, abstractmethod
from andante.options import Options, SystemParameters, ObjectWithTemporaryOptions
from andante.knowledge import MultipleKnowledge, TreeShapedKnowledge
from andante.logic_concepts import Clause, Constant, Variable, Function, Type
from andante.substitution import Substitution
import andante.hypothesis_metrics
from andante.live_log import LiveLog
from andante.collections import OrderedSet

class Learner(ObjectWithTemporaryOptions, ABC):
    def __init__(self, options=None):
        super().__init__(options)
        
    @abstractmethod
    def induce(self, examples, modes, knowledge, solver, **temp_options):
        pass


class ProgolLearner(Learner):
    """ 
    Inductive logic learner as described by S. Muggleton in 'Inverse entailment
    and progol.' 1995 available at
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.31.1630&rep=rep1&type=pdf
    """
    
    def __init__(self, **options):
        super().__init__(**options)
        self.logs = list()
        
    def add_log(self):
        """ Create new log """
        if self.options.logging:
            self.logs.append(LiveLog())
            
    def beg_child(self, *args, **kwargs):
        if self.options.logging: return self.logs[-1].beg_child(*args, **kwargs)
            
    def end_child(self, *args, **kwargs):
        if self.options.logging: return self.logs[-1].end_child(*args, **kwargs)
    
    def add_eventlog(self, event_name, value, display_fun=str):
        """ 
        Add an eventlog to the last log (only if self.options.keep_logs is true)
        Print the eventlog to the screen (only if self.options.verboseprint > 1)
        """
        self.verboseprint('%s: %s' % (event_name, display_fun(value)))
        if self.options.logging:
            self.logs[-1].add_eventlog(event_name, value)
        
    def build_bottom_i(self, e, M, B, solver):
        """ 
        For better understanding, read this function along Fig.1. 'Algorithm for constructing bottom' 
        in page 14 of document tutorial4.4.pdf 

        Parameters
        ----------
        e: andante.logic_concepts.Clause object
            A single example
        M: andante.mode.ModeCollection object
            The set of all modes
        B: andante.knowledge.Knowledge object
            The background knowledge
        solver: andante.solver.Solver object
            The engine to verify expressions
        """
        
        # 1. Add e_bar to the background knowledge
        # TODO inset a_bar
        e_knowledge = TreeShapedKnowledge([Clause(b,[]) for b in e.body], options=self.options)
        B = MultipleKnowledge(B, e_knowledge, options=self.options)
        
        # 2. Initialize InTerms and the bottom clause
        InTerms, bottom = set(), Clause(None, [])
        
        # 3. Find the first head mode declaration h such that h subsumes a with substitution theta
        # a: father_of(paul, georges)
        # m: modeh(*,father_of(+person, -person))
        # m.atom: father_of(+person, -person)
        # am: father_of(A,B)
        a  = e.head
        m  = M.get_modeh(a)
        am = m.instantiate()
        
        # s: empyt substitution
        s  = Substitution()
        am = s.rename_variables(am)
        
        # type_subst: {A/+person, B/-person}
        # theta: {A/paul, B/georges}
        type_subst = s.copy()
        type_subst.unify(am, m.atom)
        theta = s.copy()
        theta.unify(am, a)
        
        # s: {A/Paul, B/Georges}
        # InTerms: {paul}
        for v,t in theta.subst.items():
            if type_subst[v].sign=="#": s.subst[v] = t
            else:                       s.subst[v] = Variable(t.to_variable_name())
            if type_subst[v].sign=="+": InTerms.add(t)
        h = s.substitute(am)
        bottom.head = h

        # 4. Modeb
        for i in range(self.options.i):
            next_InTerms = set()
            for modeb in M.get_modeb_from_modeh(m):
                
                # For every possible substitution theta of variables corresponding 
                # to +type by terms from the set InTerms
                s, am = Substitution.from_mode(modeb)
                in_var = [v for v in s if s[v].sign=='+']
                for skolems in itertools.product(InTerms, repeat=len(in_var)):
                    theta = s.copy()
                    theta.subst = {v:skolem for v, skolem in zip(in_var, skolems)}
                    q = theta.substitute(am)

                    # Repeat a maximum of recall times
                    Theta_prime = solver.query(q, B, verbose=0)
                    
                    for theta_prime in itertools.islice(Theta_prime, modeb.recall):
                        
                        theta_final = s.copy()
                        theta_final.subst = dict()
                        
                        for v, t in itertools.chain(theta.subst.items(), theta_prime.subst.items()):
                            if v not in s: continue
                            if s[v].sign=='#': theta_final.subst[v] = t
                            else:              theta_final.subst[v] = Variable(t.to_variable_name())
                            if s[v].sign=='-': next_InTerms.add(t)
                        
                        b = theta_final.substitute(am)
                        if b not in bottom.body:
                            bottom.body.append(b)
                        
            InTerms = next_InTerms
        
        return bottom
    
    def build_hypothesis(self, examples, modes, bottom_i, knowledge, solver):
        """ Lattice search algorithm

        Given some bottom_i, builds a new clause that covers all positive
        examples but no negative examples. See above for the paper reference.
        """
        HM = self.options.hmetric
        if not isinstance(HM, andante.hypothesis_metrics.HypothesisMetric):
            HM = getattr(andante.hypothesis_metrics, HM)
        hm = HM(knowledge, examples, modes, bottom_i, solver, self.options)
        
        s0 = hm.State(Clause(bottom_i.head, []))
        self.add_eventlog('Metrics', s0.metrics_info())
        Open = OrderedSet({s0})
        Closed = OrderedSet()
        for _ in range(100):
            s = hm.best(Open)
            Open.remove(s)
            Closed.add(s)
            
            if not hm.prune(s):
                for s_new in hm.rho(s):
                    if s_new not in Open and s_new not in Closed:
                        self.add_eventlog('Candidate', s_new)
                        Open.add(s_new)
                
            if hm.terminated(Closed, Open):
                Closed = OrderedSet([s for s in Closed if s.n==0]) # Only keep candidates that cover no negative examples
                if not Closed:
                    return None
                    
                sbest = hm.best(Closed)
                c = sbest.clause
                return c
            
            if not Open:
                return None            
            
    def induce(self, examples, modes, knowledge, solver, **temp_options):
        """ Main algorithm of the learning process 

        This is the implementation of the cover set algorithm. This is the
        function called first when learning new clauses.

        Parameters
        ----------
        examples : dict
            Dictionnary containing the sets of positive and negative examples.
        modes : andante.mode.ModeCollection
            All modes and determinations that shapes the possible learned
            clauses.
        knowledge : andante.knowledge.Knowledge
            The background knowledge
        solver :
            The deduction engine
        """
        self.add_temporary_options(**temp_options)
        
        log_options = self.options.copy()
        self.add_temporary_options(verbose=0)
        self.add_log()
        self.add_eventlog('Knowledge', knowledge.copy())
        self.add_eventlog('Modes', modes)
        self.add_eventlog('Options', log_options)
        self.rem_temporary_options()
        
        self.beg_child('Iterations')
        nclause = 0
        learned_knowledge = TreeShapedKnowledge(options=knowledge.options)
        whole_knowledge = MultipleKnowledge(knowledge, learned_knowledge)
        while examples['pos'] and nclause<SystemParameters.maxclauses:            
            # Select 1 example
            e1 = examples['pos'][0]
            
            self.beg_child(e1)
            display_examples = lambda E: '%d positives - %d negatives' % (len(E['pos']), len(E['neg']))
            self.add_eventlog('Examples', examples, display_examples)            
            self.add_eventlog('Current example', e1)
            
            # Construct bottom_i
            bottom_i = self.build_bottom_i(e1, modes, whole_knowledge, solver)
            if SystemParameters.generic_name_for_variable:
                bottom_i = Substitution.generic_name_for_variables(bottom_i)
            self.add_eventlog('Bottom_i',bottom_i)
            
            # Build hypothesis
            self.beg_child('States')
            C = self.build_hypothesis(examples, modes, bottom_i, whole_knowledge, solver)
            self.end_child()
            self.add_eventlog('Clause', C)
            
            # Add hypothesis to background knowledge
            if C is not None:
                learned_knowledge.add(C)
            examples = {'pos':[e for e in examples['pos'] if not solver.succeeds_on(e.head, whole_knowledge, verbose=0)],
                        'neg':examples['neg']}
            
            nclause += 1
            self.verboseprint('')
            self.end_child()
        self.end_child()    
        
        self.add_eventlog('Learned knowledge', learned_knowledge)    
        if self.options.update_knowledge:
            for c in learned_knowledge:
                knowledge.add(c)
    
        #add already background knoweldge already existing rules
        background_rules = []
        rule_pattern = re.compile(r'complication\(\w+\) :- .*\.')

        for rule in knowledge:
            if rule_pattern.match(str(rule)):
                background_rules.append(rule)
        
        # Extract and add background knowledge rules to the learned knowledge
        for rule in background_rules:
            if rule not in learned_knowledge:
                learned_knowledge.add(rule)

        self.rem_temporary_options()
        
        return learned_knowledge
