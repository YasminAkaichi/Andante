import itertools
from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.knowledge import MultipleKnowledge, LogicProgram
from aloe.clause import Clause, Constant, Variable, Function, Type
from aloe.substitution import Substitution
import aloe.hypothesis_metrics

class Learner(ABC):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        self.options = options if options else Options()
        
    @abstractmethod
    def induce(self, examples, modes, knowledge, solver, verbose=None):
        pass
            
class ProgolLearner(Learner):
    """ 
    Inductive logic learner as described by S. Muggleton in 'Inverse entailment and progol.' 1995
    available at http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.31.1630&rep=rep1&type=pdf
    """
        
    def build_bottom_i(self, e, M, B, solver):
        """ 
        For better understanding, read this function along Fig.1. 'Algorithm for constructing bottom' 
        in page 14 of document tutorial4.4.pdf 
        Inputs:
        - e: a single example (Clause object)
        - M: the set of all modes (ModeCollection object)
        - B: the background knowledge (Knowledge object)
        - solver: the engine to verify expressions (Solver object)
        """
        
        # 1. Add e_bar to the background knowledge
        e_knowledge = LogicProgram([e], options=self.options)
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
        
        for v,t in theta.subst.items():
            if type_subst[v].sign=="#": s[v] = t
            else:                       s[v] = Variable(t.to_variable_name())
            if type_subst[v].sign=="+": InTerms.add(t)
        # s: {A/Paul, B/Georges}
        # InTerms: {paul}
        h = s.apply_subst(am)
        bottom.head = h

        # 4. Modeb
        for i in range(self.options.i):
            next_InTerms = set()
            for modeb in M.get_modeb(m):
                
                # For every possible substitution theta of variables corresponding 
                # to +type by terms from the set InTerms
                s, am = Substitution.from_mode(modeb)
                in_var = [v for v in s if s[v].sign=='+']
                for skolems in itertools.product(InTerms, repeat=len(in_var)):
                    theta = s.copy()
                    theta.subst = {v:skolem for v, skolem in zip(in_var, skolems)}
                    q = theta.apply_subst(am)

                    # Repeat a maximum of recall times
                    Theta_prime = solver.query(q, B, verbose=0)
                    
                    for theta_prime in itertools.islice(Theta_prime, modeb.recall):
                        
                        theta_final = s.copy()
                        theta_final.subst = dict()
                        
                        for v, t in itertools.chain(theta.subst.items(), theta_prime.subst.items()):
                            if v not in s: continue
                            if s[v].sign=='#': theta_final[v] = t
                            else:              theta_final[v] = Variable(t.to_variable_name())
                            if s[v].sign=='-': next_InTerms.add(t)
                        
                        b = theta_final.apply_subst(am)
                        bottom.body.append(b)
                        
            InTerms = next_InTerms
        
        return bottom
    
    def build_hypothesis(self, examples, bottom_i, knowledge, solver):
        options = self.options
        verboseprint = print if self.verbose==1 else lambda *a, **k: None                
        
        HM = self.options.hmetric
        if not isinstance(HM, aloe.hypothesis_metrics.HypothesisMetric):
            HM = getattr(aloe.hypothesis_metrics, HM)
        hm = HM(knowledge, examples, bottom_i, solver, options)
        
        verboseprint('[  c,  h,  p,  n,  g,  f]')
        
        s0 = hm.State(Clause(bottom_i.head, []))
        Open = {s0}
        Closed = set()
        for _ in range(100):
            s = hm.best(Open)
            verboseprint(s)
            Open.remove(s)
            Closed.add(s)
            
            if not hm.prune(s):
                Open = (Open | set(list(hm.rho(s)))) - Closed
                
            if hm.terminated(Closed, Open):
                return hm.best(Closed).clause
            
            if not Open:
                return None
        
    def induce(self, examples, modes, knowledge, solver, verbose=None):
        self.verbose = verbose if verbose is not None else self.options.verbose
        verboseprint = print if self.verbose==1 else lambda *a, **k: None                        
        
        nclause = 0
        while examples['pos'] and nclause<self.options.maxclauses:
            verboseprint('#examples: %2d pos, %2d neg' % (len(examples['pos']),len(examples['neg'])))
            e1 = examples['pos'][0]
            verboseprint('Example considered:',e1)
            bottom_i = self.build_bottom_i(e1, modes, knowledge, solver)
            verboseprint('Bottom_i',bottom_i)
            C = self.build_hypothesis(examples, bottom_i, knowledge, solver)
            verboseprint('Clause found', C)
            knowledge.add(C)
            examples['pos'] = [e for e in examples['pos'] if not solver.solve(e.head, knowledge, verbose=0)]
            
            verboseprint('\n'*2)
            nclause += 1
            
        return C
    
        
        
        